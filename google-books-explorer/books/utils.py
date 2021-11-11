import os

import dotenv
import requests
import requests_cache

dotenv.load_dotenv()
requests_cache.install_cache('gbooks')

API_KEY = os.environ.get('API_KEY')


def call_books_api(query, page=0):
    url = 'https://www.googleapis.com/books/v1/volumes'

    try:
        page = int(page)
    except TypeError:
        raise ValueError('Page must be an integer.')

    if page == 0:
        start_index = 0
    else:
        start_index = page * 15  # looping through items, not pages

    params = {
        'key': API_KEY,
        'q': query,
        'maxResults': 15,
        'startIndex': start_index,
        'fields': 'items(id,volumeInfo(title,authors))',
    }
    r = requests.get(url, params=params)
    items = r.json().get('items')
    books = []

    if items:
        for item in items:
            book = {}
            info = item['volumeInfo']
            book['title'] = info.get('title')
            authors = info.get('authors')
            book['authors'] = ', '.join(authors) if authors else []
            book['link'] = f"https://books.google.ru/books/?id={item['id']}"
            books.append(book)
    return books
