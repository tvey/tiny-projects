import os

import dotenv
import requests

dotenv.load_dotenv()

API_KEY = os.environ.get('API_KEY')


def call_books_api(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'key': API_KEY,
        'q': query,
        'maxResults': 15,
        # 'startIndex': 0,  # todo: go through pages, infinite scroll
    }
    r = requests.get(url, params=params)
    items = r.json().get('items')
    books = []

    if items:
        for item in items:
            book = {}
            info = item['volumeInfo']
            book['title'] = info.get('title')
            book['subtitle'] = info.get('subtitle')
            authors = info.get('authors')
            book['authors'] = ', '.join(authors) if authors else []
            book['description'] = info.get('description')
            book['link'] = f"https://books.google.ru/books/?id={item['id']}"
            book['piblished_date'] = info.get('publishedDate')
            books.append(book)
    return books
