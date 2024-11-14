import os
import json
import argparse
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
from collections import defaultdict


class JSONHTMLParser:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def parse_json_html(self, document_path):
        try:
            with open(document_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error parsing {document_path}: {e}")
            return []

        if 'content' not in data:
            return []

        soup = BeautifulSoup(data['content'], 'lxml')
        tokens = []

        for tag in soup.find_all(['b', 'h1', 'h2', 'h3', 'title', 'p']):
            tag_text = tag.get_text()
            for word in self.tokenize(tag_text):
                stemmed_word = self.stemmer.stem(word)
                tokens.append(stemmed_word)

        return tokens

    def tokenize(self, text):
        return [word.lower() for word in text.split() if word.isalnum()]


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)

    def add_document(self, doc_id, tokens):
        tf_dict = defaultdict(int)
        for token in tokens:
            tf_dict[token] += 1  # Count occurrences of each token

        for token, tf in tf_dict.items():
            posting = {'doc_id': doc_id, 'tf': tf}
            self.index[token].append(posting)

    def save_index_with_analytics(self, file_path):
        
        with open(file_path, 'w') as file:
            for term, postings in self.index.items():
                postings_str = "; ".join([f"(doc_id: {posting['doc_id']}, tf: {posting['tf']})" for posting in postings])
                file.write(f"{term}: {postings_str}\n")
                
        num_docs = len(set([posting['doc_id'] for postings in self.index.values() for posting in postings]))
        num_unique_tokens = len(self.index)
        index_size_kb = os.path.getsize(file_path) / 1024
        analytics = f"Documents indexed: {num_docs}\nUnique tokens: {num_unique_tokens}\nSize: {index_size_kb:.2f} KB\n"

        with open(file_path, 'w') as file:
            file.write(analytics)

        print(f"Index saved to {file_path}, size: {index_size_kb:.2f} KB")


def process_folder(folder_path, index):
    parser = JSONHTMLParser()
    processed_files = 0

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                tokens = parser.parse_json_html(file_path)
                index.add_document(filename, tokens)
                processed_files += 1


def main():
    parser = argparse.ArgumentParser(description="Build an inverted index from JSON files containing HTML content.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing JSON files.")
    parser.add_argument("output_file", type=str, help="Path to save the inverted index (JSON format).")
    args = parser.parse_args()

    index = InvertedIndex()
    
    process_folder(args.folder_path, index)
    
    index.save_index_with_analytics(args.output_file)


if __name__ == "__main__":
    main() #To use: python3 invertedIndex.py "path to directory containing subdirectories and files to parse" "path to output"
