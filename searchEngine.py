import json
import math
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

class SearchEngine:
    def __init__(self, index_path):
        self.index_data = self.load_index(index_path)
        self.index = self.index_data['index']
        self.doc_urls = self.index_data['doc_urls']
        self.stemmer = PorterStemmer()
        self.db = MongoClient("localhost", 27017)
        self.collection = self.db.searchEngine.finalIndex
        self.document_count = self.db.searchEngine.finalIndexMetadata.find_one()["doc_count"]

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

        token_docs = {
            doc["_id"]: doc
            for doc in self.collection.find({"_id": {"$in": query_tokens}})
        }

        for token in query_tokens:
            if token not in token_docs:
                continue
            postings = token_docs[token]
            idf = math.log10(self.document_count / postings['document_freq'])

            for doc_id, doc_data in postings["doc_ids"].items():
                tf_idf = doc_data['tf_idf']
                scores[doc_id] += query_weights[token] * tf_idf

        ranked_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(self.doc_urls[doc_id], score) for doc_id, score in ranked_results[:top_k]]


@app.route("/process-query", methods=["POST"])
def process_query():
    query = request.json
    startTime = time.perf_counter()
    results = engine.search(query)
    endTime = time.perf_counter()
    totalTime = (endTime - startTime) * 1000
    return jsonify(results, totalTime)

if __name__ == "__main__":
    engine = SearchEngine("/Users/bevinhuynh/SearchEngine/final_index.json")
    app.run(host='0.0.0.0', port=1410)