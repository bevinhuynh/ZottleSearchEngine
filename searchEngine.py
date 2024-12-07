# import json
# import math
# from collections import defaultdict
# from nltk.stem.porter import PorterStemmer


# class SearchEngine:
#     def __init__(self, index_path):
#         self.index_data = self.load_index(index_path)
#         self.index = self.index_data['index']
#         self.doc_urls = self.index_data['doc_urls']
#         self.stemmer = PorterStemmer()

#     def load_index(self, index_path):
#         with open(index_path, 'r', encoding='utf-8') as file:
#             return json.load(file)

#     def preprocess_query(self, query):
#         tokens = query.lower().split()
#         return [self.stemmer.stem(token) for token in tokens if token.isalnum()]

#     def search(self, query, top_k=10):
#         query_tokens = self.preprocess_query(query)
#         scores = defaultdict(float)
#         query_weights = {token: 1 + math.log10(query_tokens.count(token)) for token in query_tokens}

#         for token in query_tokens:
#             if token not in self.index:
#                 continue
#             postings = self.index[token]['doc_ids']
#             idf = math.log10(self.index_data['doc_count'] / self.index[token]['document_freq'])
#             for doc_id, doc_data in postings.items():
#                 tf_idf = doc_data['tf_idf']
#                 scores[doc_id] += query_weights[token] * tf_idf

#         ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#         return [(self.doc_urls[doc_id], score) for doc_id, score in ranked_results[:top_k]]


# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("index_path", type=str, help="Path to the JSON index file.")
#     parser.add_argument("query", type=str, help="Search query.")
#     args = parser.parse_args()

#     engine = SearchEngine(args.index_path)
#     results = engine.search(args.query)
#     for rank, (url, score) in enumerate(results, 1):
#         print(f"{rank}. URL: {url}, Score: {score:.4f}")
import json
import math
from collections import defaultdict
from nltk.stem.porter import PorterStemmer


class SearchEngine:
    def __init__(self, index_path):
        self.index_data = self.load_index(index_path)
        self.index = self.index_data['index']
        self.doc_urls = self.index_data['doc_urls']
        self.stemmer = PorterStemmer()

    def load_index(self, index_path):
        with open(index_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def preprocess_query(self, query):
        tokens = query.lower().split()
        return [self.stemmer.stem(token) for token in tokens if token.isalnum()]

    def search(self, query, top_k=10):
        query_tokens = self.preprocess_query(query)
        scores = defaultdict(float)
        query_weights = {token: 1 + math.log10(query_tokens.count(token)) for token in query_tokens}

        for token in query_tokens:
            if token not in self.index:
                continue
            postings = self.index[token]['doc_ids']
            idf = math.log10(self.index_data['doc_count'] / self.index[token]['document_freq'])
            for doc_id, doc_data in postings.items():
                tf_idf = doc_data['tf_idf']
                scores[doc_id] += query_weights[token] * tf_idf

        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.doc_urls[doc_id], score) for doc_id, score in ranked_results[:top_k]]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("index_path", type=str, help="Path to the JSON index file.")
    parser.add_argument("query", type=str, help="Search query.")
    args = parser.parse_args()

    engine = SearchEngine(args.index_path)
    results = engine.search(args.query)
    for rank, (url, score) in enumerate(results, 1):
        print(f"{rank}. URL: {url}, Score: {score:.4f}")

