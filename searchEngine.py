import json
from math import log
from collections import defaultdict
from nltk.stem.porter import PorterStemmer


class SearchEngine:
    def __init__(self, index_path):
        self.index, self.doc_urls = self.load_index(index_path)

    def load_index(self, index_path):
        #loads in inverted index (.json file) to create a dictionary
        try:
            with open(index_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data['index'], data['doc_urls']
                #data['index']: The inverted index (maps terms to their document postings).
                #data['doc_urls']: Maps document IDs to their URLs
        except FileNotFoundError:
            print(f"Index file {index_path} not found.")
            return {}, {}

    def calculate_idf(self, term):
        # Calculate Inverse Document Frequency (IDF) -- measures how rare/unique the term is across all documents
        doc_freq = len(self.index.get(term, []))
        if doc_freq == 0:
            return 0
        return log(self.doc_count / doc_freq)

    @property #makes it read-only -- cleaner code
    def doc_count(self):
        return len(self.doc_urls)

    def search(self, query):
        #The search method processes a user's query and finds the most relevant documents using TF-IDF scoring.
        stemmer = PorterStemmer()
        query_terms = [stemmer.stem(term.lower()) for term in query.split() if term.isalnum()]
        if not query_terms:
            print("Empty query!")
            return []

        scores = defaultdict(float)
        for term in query_terms:
            if term not in self.index:
                continue

            idf = self.calculate_idf(term)
            for posting in self.index[term]:
                tf = posting['tf']
                doc_id = posting['doc_id']
                scores[doc_id] += tf * idf  # TF-IDF score

        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.doc_urls[doc_id], score) for doc_id, score in ranked_results]

    def display_results(self, results, top_n=5):
        if not results:
            print("No results found.")
            return

        print(f"Top {min(top_n, len(results))} results:")  #displays top 5 results
        for rank, (url, score) in enumerate(results[:top_n], start=1):
            print(f"{rank}. {url} (Score: {score:.4f})")


def main():
    import argparse
    import time

    parser = argparse.ArgumentParser(description="Terminal-based Search Engine")
    parser.add_argument("index_path", type=str, help="Path to the saved inverted index.")
    args = parser.parse_args()

    engine = SearchEngine(args.index_path)

    while True:
        query = input("Enter query (type exit to stop): ")
        if query.lower() == 'exit':
            print("Exiting search engine.")
            break
        startTime = time.perf_counter()
        results = engine.search(query)
        endTime = time.perf_counter()

        totalTime = (endTime - startTime) * 1000 #calculates time in millisecond
        engine.display_results(results)
        print(f"Query processed in {totalTime:.2f} ms")

if __name__ == "__main__":
    main()
