import os
import json
import math
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: {'token_freq': 0, 'document_freq': 0, 'doc_ids': {}})
        self.doc_count = 0  # Total number of documents
        self.doc_urls = {}  # Map doc_id to URL
        self.stemmer = PorterStemmer()

    def add_document(self, doc_id, content, url):
        soup = BeautifulSoup(content, 'lxml')
        self.doc_urls[doc_id] = url

        # Define tag weights
        tag_weights = {
            'title': 5,
            'h1': 4,
            'h2': 3,
            'h3': 2,
            'strong': 2,
            'p': 1
        }

        term_freqs = defaultdict(int)

        # Extract and weigh tokens
        for tag, weight in tag_weights.items():
            for element in soup.find_all(tag):
                tokens = self.tokenize_and_stem(element.get_text())
                for token in tokens:
                    term_freqs[token] += weight

        # Update index
        for token, freq in term_freqs.items():
            self.index[token]['token_freq'] += freq
            if doc_id not in self.index[token]['doc_ids']:
                self.index[token]['doc_ids'][doc_id] = {'freq': 0, 'tf_idf': 0}
                self.index[token]['document_freq'] += 1
            self.index[token]['doc_ids'][doc_id]['freq'] = freq

        self.doc_count += 1

    def tokenize_and_stem(self, text):
        tokens = [word.lower() for word in text.split() if word.isalnum()]
        return [self.stemmer.stem(token) for token in tokens]

    def save_partial_index(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'index': self.index,
                'doc_urls': self.doc_urls,
                'doc_count': self.doc_count
            }, file, indent=4)
        print(f"Partial index saved to {file_path}")

    def merge_partial_indexes(self, partial_index_files, merged_index_path):
        merged_index = defaultdict(lambda: {'token_freq': 0, 'document_freq': 0, 'doc_ids': {}})
        doc_urls = {}
        doc_count = 0

        for partial_file in partial_index_files:
            with open(partial_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for token, entry in data['index'].items():
                    if token not in merged_index:
                        merged_index[token] = entry
                    else:
                        merged_index[token]['token_freq'] += entry['token_freq']
                        merged_index[token]['document_freq'] += entry['document_freq']
                        merged_index[token]['doc_ids'].update(entry['doc_ids'])
                doc_urls.update(data['doc_urls'])
                doc_count += data['doc_count']

        with open(merged_index_path, 'w', encoding='utf-8') as file:
            json.dump({
                'index': merged_index,
                'doc_urls': doc_urls,
                'doc_count': doc_count
            }, file, indent=4)
        print(f"Merged index saved to {merged_index_path}")

    def calculate_tfidf(self, merged_index_path):
        """
        Calculate TF-IDF values for all terms in the merged index and save the updated index.
        """
        with open(merged_index_path, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        index = data['index']
        doc_count = data['doc_count']

        # Debugging: Ensure doc_count is correct
        if doc_count == 0:
            print("Error: Document count is 0. No documents to calculate TF-IDF.")
            return

        # Iterate over all terms in the index
        for token, entry in index.items():
            # Debugging: Check document frequency
            if entry['document_freq'] == 0:
                print(f"Skipping token '{token}' with document frequency 0.")
                continue

            # Calculate IDF for the term
            idf = math.log10(doc_count / entry['document_freq'])

            # Debugging: Print IDF
            print(f"Token: {token}, IDF: {idf}")

            # Update TF-IDF for each document containing the term
            for doc_id, doc_data in entry['doc_ids'].items():
                if doc_data['freq'] > 0:  # Ensure term frequency is valid
                    tf = 1 + math.log10(doc_data['freq'])
                    doc_data['tf_idf'] = tf * idf  # Assign TF-IDF

                    # Debugging: Print TF-IDF values
                    print(f"Doc ID: {doc_id}, TF: {tf}, TF-IDF: {doc_data['tf_idf']}")
                else:
                    doc_data['tf_idf'] = 0  # Assign 0 TF-IDF if term frequency is zero

        # Save the updated index back to the file
        with open(merged_index_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)

        print("TF-IDF values calculated and saved.")




def process_folder(folder_path, partial_index_dir, batch_size=1000):
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
                    partial_path = os.path.join(partial_index_dir, f'partial_index_{processed_docs // batch_size}.json')
                    index.save_partial_index(partial_path)
                    partial_index_files.append(partial_path)
                    index = InvertedIndex()

    if processed_docs % batch_size != 0:
        partial_path = os.path.join(partial_index_dir, f'partial_index_{processed_docs // batch_size + 1}.json')
        index.save_partial_index(partial_path)
        partial_index_files.append(partial_path)

    return partial_index_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("folder_path", type=str, help="Folder containing JSON files.")
    parser.add_argument("partial_index_dir", type=str, help="Directory to save partial indexes.")
    parser.add_argument("final_index_file", type=str, help="Path to save the merged index.")
    args = parser.parse_args()

    partial_indexes = process_folder(args.folder_path, args.partial_index_dir)
    index = InvertedIndex()
    index.merge_partial_indexes(partial_indexes, args.final_index_file)
    index.calculate_tfidf(args.final_index_file)
