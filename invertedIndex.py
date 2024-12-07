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

    def save_partial_index(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'index': self.index,
                'doc_urls': self.doc_urls
            }, file, indent=4)
        print(f"Partial index saved to {file_path}")

    def merge_index(self, other_index):
        """
        Merge another InvertedIndex object into the current index.
        """
        for term, postings in other_index.index.items():
            self.index[term].extend(postings)
        self.doc_urls.update(other_index.doc_urls)
        self.doc_count += other_index.doc_count

    def save_index_with_analytics(self, file_path):
        """
        Save the final merged index and generate analytics.
        """
        # Calculate document lengths for normalization (if needed for TF-IDF)
        doc_lengths = {}
        for doc_id in self.doc_urls:
            length = 0
            for term, postings in self.index.items():
                for posting in postings:
                    if posting['doc_id'] == doc_id:
                        length += posting['tf'] ** 2  # Sum of squared term frequencies
            doc_lengths[doc_id] = length ** 0.5  # Euclidean norm

        # Save the index and metadata
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'index': self.index,
                'doc_urls': self.doc_urls,
                'doc_lengths': doc_lengths
            }, file, indent=4)

        # Generate and print analytics
        num_unique_terms = len(self.index)
        index_size_kb = os.path.getsize(file_path) / 1024
        print(f"Final index saved to {file_path}")
        print(f"Total documents: {self.doc_count}")
        print(f"Unique terms: {num_unique_terms}")
        print(f"Index size: {index_size_kb:.2f} KB")


def process_folder(folder_path, output_dir, batch_size=1000):
    parser = JSONHTMLParser()
    processed_files = 0
    batch_number = 1

    # Initialize an empty index for the current batch
    current_index = InvertedIndex()

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                tokens, url = parser.parse_json_html(file_path)
                if tokens and url:
                    current_index.add_document(filename, tokens, url)
                    processed_files += 1

                # Save partial index and reset when batch size is reached
                if processed_files % batch_size == 0:
                    partial_index_file = os.path.join(output_dir, f"partial_index_{batch_number}.json")
                    current_index.save_partial_index(partial_index_file)
                    current_index = InvertedIndex()  # Reset for the next batch
                    batch_number += 1

    # Save any remaining documents in the last batch
    if current_index.doc_count > 0:
        partial_index_file = os.path.join(output_dir, f"partial_index_{batch_number}.json")
        current_index.save_partial_index(partial_index_file)


def merge_partial_indexes(output_dir, final_index_path):
    final_index = InvertedIndex()

    for root, _, files in os.walk(output_dir):
        for filename in files:
            if filename.startswith("partial_index_") and filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                with open(file_path, 'r', encoding='utf-8') as file:
                    partial_data = json.load(file)
                    partial_index = InvertedIndex()
                    partial_index.index = defaultdict(list, partial_data['index'])
                    partial_index.doc_urls = partial_data['doc_urls']
                    partial_index.doc_count = len(partial_index.doc_urls)

                    final_index.merge_index(partial_index)

    # Save the final merged index
    final_index.save_index_with_analytics(final_index_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build and save an inverted index from JSON files.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing JSON files.")
    parser.add_argument("output_dir", type=str, help="Directory to save partial index files.")
    parser.add_argument("final_index_file", type=str, help="Path to save the final merged index (JSON format).")
    parser.add_argument("--batch_size", type=int, default=1000, help="Number of files per batch.")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Process files and save partial indexes
    process_folder(args.folder_path, args.output_dir, args.batch_size)

    # Merge all partial indexes into a final index
    merge_partial_indexes(args.output_dir, args.final_index_file)


if __name__ == "__main__":
    main()
