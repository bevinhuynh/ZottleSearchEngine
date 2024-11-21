import os
import json
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer


class JSONHTMLParser:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def parse_json_html(self, document_path):
        try:
            with open(document_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error parsing {document_path}: {e}")
            return [], None

        if 'content' not in data or 'url' not in data:
            return [], None

        soup = BeautifulSoup(data['content'], 'lxml')
        tokens = []

        # Assign weights to tags
        tag_weights = {'title': 5, 'h1': 4, 'h2': 3, 'h3': 2, 'p': 1, 'b': 1}

        for tag, weight in tag_weights.items():
            for element in soup.find_all(tag):
                for word in self.tokenize(element.get_text()):
                    stemmed_word = self.stemmer.stem(word)
                    tokens.extend([stemmed_word] * weight)  # Weighted tokens

        return tokens, data['url']

    def tokenize(self, text):
        return [word.lower() for word in text.split() if word.isalnum()]


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.doc_count = 0  # Total number of documents
        self.doc_urls = {}  # Map doc_id to URL

    def add_document(self, doc_id, tokens, url):
        tf_dict = defaultdict(int)
        for token in tokens:
            tf_dict[token] += 1

        for token, tf in tf_dict.items():
            posting = {'doc_id': doc_id, 'tf': tf}
            self.index[token].append(posting)

        self.doc_count += 1
        self.doc_urls[doc_id] = url

    def save_index_with_analytics(self, file_path):
        json_file_path = file_path + "_Data.json"
        analytics_file_path = file_path + "_analytics.txt"

        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump({'index': self.index, 'doc_urls': self.doc_urls}, file, indent=4)

        num_docs = self.doc_count
        num_unique_tokens = len(self.index)
        index_size_kb = os.path.getsize(json_file_path) / 1024
        analytics = f"Documents indexed: {num_docs}\nUnique tokens: {num_unique_tokens}\nSize: {index_size_kb:.2f} KB\n"

        with open(analytics_file_path, 'w') as file:
            file.write(analytics)

        print(f"Index saved to {file_path}, size: {index_size_kb:.2f} KB")


def process_folder(folder_path, index):
    parser = JSONHTMLParser()
    processed_files = 0

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                tokens, url = parser.parse_json_html(file_path)
                if tokens and url:
                    index.add_document(filename, tokens, url)
                    processed_files += 1


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build and save an inverted index from JSON files.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing JSON files.")
    parser.add_argument("output_file", type=str, help="Path to save the inverted index (JSON format).")
    args = parser.parse_args()

    index = InvertedIndex()
    process_folder(args.folder_path, index)
    index.save_index_with_analytics(args.output_file)


if __name__ == "__main__":
    main()
