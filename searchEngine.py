import json
import time
from math import log
from collections import defaultdict
from nltk.stem.porter import PorterStemmer


class SearchEngine:
    def __init__(self, index_path):
        self.index, self.doc_urls, self.doc_lengths = self.load_index(index_path)

    def load_index(self, index_path):
        """
        Load the inverted index and document metadata.
        """
        try:
            with open(index_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                index = data['index']
                doc_urls = data['doc_urls']
                doc_lengths = data.get('doc_lengths', {})  # Precomputed lengths for normalization
                return index, doc_urls, doc_lengths
        except FileNotFoundError:
            print(f"Index file {index_path} not found.")
            return {}, {}, {}

    def calculate_tf_idf(self, term, tf, doc_count, doc_freq):
        """
        Calculate the TF-IDF score for a term.
        """
        if doc_freq == 0:
            return 0
        idf = log(doc_count / doc_freq)  # Inverse Document Frequency
        return tf * idf  # Term Frequency-Inverse Document Frequency

    @property
    def doc_count(self):
        """
        Total number of documents.
        """
        return len(self.doc_urls)

    def search(self, query):
        """
        Perform a TF-IDF-based search.
        """
        stemmer = PorterStemmer()
        query_terms = [stemmer.stem(term.lower()) for term in query.split() if term.isalnum()]
        if not query_terms:
            print("Empty query!")
            return []

        scores = defaultdict(float)
        for term in query_terms:
            if term not in self.index:
                continue

            postings = self.index[term]
            doc_freq = len(postings)

            for posting in postings:
                doc_id = posting['doc_id']
                tf = posting['tf']
                tf_idf = self.calculate_tf_idf(term, tf, self.doc_count, doc_freq)
                scores[doc_id] += tf_idf  # Accumulate TF-IDF score

        # Normalize scores by document length
        for doc_id in scores:
            if doc_id in self.doc_lengths:
                scores[doc_id] /= self.doc_lengths[doc_id]

        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.doc_urls[doc_id], score) for doc_id, score in ranked_results]

    def evaluate_queries(self, queries):
        """
        Evaluate a set of queries for performance and effectiveness.
        """
        results = []
        for query in queries:
            start_time = time.perf_counter()
            result = self.search(query)
            end_time = time.perf_counter()
            runtime = (end_time - start_time) * 1000  # Convert to milliseconds
            results.append((query, len(result), runtime))
        return results

    def display_results(self, results, top_n=5):
        """
        Display the top N search results.
        """
        if not results:
            print("No results found.")
            return

        print(f"Top {min(top_n, len(results))} results:")
        for rank, (url, score) in enumerate(results[:top_n], start=1):
            print(f"{rank}. {url} (Score: {score:.4f})")

    def save_analytics(self, query_results, output_path):
        """
        Save query evaluation analytics to a file.
        """
        with open(output_path, 'w') as file:
            file.write("Query,Results,Runtime (ms)\n")
            for query, num_results, runtime in query_results:
                file.write(f"{query},{num_results},{runtime:.2f}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TF-IDF Based Search Engine with Query Evaluation")
    parser.add_argument("index_path", type=str, help="Path to the saved inverted index.")
    parser.add_argument("--queries", type=str, help="Path to a file containing evaluation queries.")
    parser.add_argument("--analytics", type=str, help="Path to save analytics results.")
    args = parser.parse_args()

    engine = SearchEngine(args.index_path)

    # Load evaluation queries
    if args.queries:
        with open(args.queries, 'r') as file:
            queries = [line.strip() for line in file.readlines()]

        query_results = engine.evaluate_queries(queries)
        if args.analytics:
            engine.save_analytics(query_results, args.analytics)
            print(f"Analytics saved to {args.analytics}")

    # Interactive search mode
    while True:
        query = input("Enter query (type exit to stop): ")
        if query.lower() == 'exit':
            print("Exiting search engine.")
            break
        results = engine.search(query)
        engine.display_results(results)


if __name__ == "__main__":
    main()
