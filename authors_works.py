# October 19 lecture demo on apis
import argparse
import requests
import os.path
import json

scripts_path = os.path.dirname(os.path.realpath(__file__))
raw_data_path = os.path.join(scripts_path, 'data')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--author', type=str, help='name of the author to search for')
    args = parser.parse_args()

    author_name = args.author
    if author_name is None:
        author_name =r'jane%20austen'
    query_url = f'https://openlibrary.org/search/authors.json?q={author_name}'
    r = requests.get(query_url)
    print(r.text)
    author_data = r.json()
    author_key = author_data['docs'][0]['key']
    books_url = f'https://openlibrary.org/authors/{author_key}/works.json'
    r = requests.get(books_url)
    books_data = r.json()
    f_name = f"author_{author_key}_books.json"
    with open(os.path.join(raw_data_path, f_name), 'w') as fi:
        json.dump(books_data, fi)
        
    
if __name__ == "__main__":
    main()
    