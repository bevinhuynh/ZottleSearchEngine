import os
import json
import math
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from pymongo import MongoClient

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: {'token_freq': 0, 'document_freq': 0, 'doc_ids': {}})
        self.doc_count = 0  # total # of documents
        self.doc_urls = {}  # dictionary to map doc_id to URLs
        self.stemmer = PorterStemmer()
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.searchEngine

    def add_document(self, doc_id, content, url):
        soup = BeautifulSoup(content, 'lxml')
        self.doc_urls[str(doc_id)] = url

        tag_weights = {
            'title': 5,
            'h1': 4,
            'h2': 3,
            'h3': 2,
            'strong': 2,
            'p': 1  
        }

        term_freqs = defaultdict(int)

        for tag, weight in tag_weights.items():
            for element in soup.find_all(tag):
                tokens = self.tokenize_and_stem(element.get_text())
                for token in tokens:
                    term_freqs[token] += weight

        for token, freq in term_freqs.items():
            self.index[token]['token_freq'] += freq
            if doc_id not in self.index[token]['doc_ids']:
                self.index[token]['doc_ids'][str(doc_id)] = {'freq': 0, 'tf_idf': 0}
                self.index[token]['document_freq'] += 1
            self.index[token]['doc_ids'][str(doc_id)]['freq'] = freq

        self.doc_count += 1

    def tokenize_and_stem(self, text):
        tokens = [word.lower() for word in text.split() if word.isalnum()]
        return [self.stemmer.stem(token) for token in tokens]

    def save_partial_index(self):
        term = {
            "index": self.index,
            "doc_urls": self.doc_urls,
            'doc_count': self.doc_count
        }
        partialIndexes = self.db.partialIndexes
        partialIndex_id = partialIndexes.insert_one(term).inserted_id
        print(f"Partial index saved to the database")
    
    def merge_partial_indexes(self):
        merged_index = defaultdict(lambda: {'token_freq': 0, 'document_freq': 0, 'doc_ids': {}})
        doc_urls = {}
        doc_count = 0
        partialIndexes = self.db.partialIndexes.find()

        for partial_index in partialIndexes:
            for token, entry in partial_index['index'].items():
                if token not in merged_index:
                    merged_index[token] = entry
                else:
                    merged_index[token]['token_freq'] += entry['token_freq']
                    merged_index[token]['document_freq'] += entry['document_freq']

                    for doc_id, doc_data in entry['doc_ids'].items():
                        if doc_id in merged_index[token]['doc_ids']:
                            merged_index[token]['doc_ids'][doc_id]['freq'] += doc_data['freq']
                        else:
                            merged_index[token]['doc_ids'][doc_id] = doc_data
            doc_urls.update(partial_index['doc_urls'])
            doc_count += partial_index['doc_count']

        self.save_final_index_by_token(merged_index)

        metadata = {
            "doc_urls": doc_urls,
            "doc_count": doc_count
        }
        self.db.finalIndexMetadata.insert_one(metadata)
        print("Final index saved with each token as a separate document.")

    def save_final_index_by_token(self, final_index):
        finalIndex = self.db.finalIndex

        # Insert each token as a separate document
        for token, data in final_index.items():
            finalIndex.insert_one({
                "_id": token,  # Use the token as the unique identifier
                "token_freq": data["token_freq"],
                "document_freq": data["document_freq"],
                "doc_ids": data["doc_ids"]
            })
        print("All tokens saved as separate documents.")

    #     # Calculate tf-idf scores
    def calculate_tfidf(self):
        final_index = self.db.finalIndex.find()

        for document in final_index:
            token = document["_id"]
            if document["document_freq"] == 0:
               print(f"Skipping token '{token}' with document frequency 0.")
               continue
            idf = math.log10(55000 / document['document_freq'])
            updates = {}

            for doc_id, doc_data in document["doc_ids"].items():
                if doc_data['freq'] > 0: 
                    tf = 1 + math.log10(doc_data['freq'])
                    doc_data['tf_idf'] = tf * idf  

                else:
                    doc_data['tf_idf'] = 0  
                updates[f"doc_ids.{doc_id}.tf_idf"] = doc_data["tf_idf"]

            if updates:
                self.db.finalIndex.update_one(
                    {"_id": token},  # Match the token document by its _id
                    {"$set": updates}  # Apply collected updates
                )

        print("TF-IDF calculation and incremental update completed.")


def process_folder(folder_path, batch_size=500):
    index = InvertedIndex()
    doc_id = 0
    processed_docs = 0
    partial_index_files = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if 'content' in data and 'url' in data:
                        index.add_document(doc_id, data['content'], data['url'])
                        doc_id += 1
                        processed_docs += 1

                if processed_docs % batch_size == 0:
                    index.save_partial_index()
                    index = InvertedIndex()
                  
    if processed_docs % batch_size != 0:
        index.save_partial_index()

    return partial_index_files

# To run code -> python3 invertedIndex.py "path to DEV folder" "path to partial_index folder" "path to final_index file (doesn't have to be created)"
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", type=str, help="Folder containing JSON files.")
    args = parser.parse_args()

    partial_indexes = process_folder(args.folder_path)
    index = InvertedIndex()
    index.merge_partial_indexes()
    index.calculate_tfidf()






