import json
import os

import dotenv
import httpx
from praw import Reddit
from prawcore.exceptions import Forbidden
from requests_html import HTMLSession

dotenv.load_dotenv()


def create_reddit_client() -> Reddit:
    client = Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        user_agent=os.environ.get('REDDIT_APP_NAME'),
    )
    return client


def get_pic_urls(client: Reddit, subreddit_name: str, limit: int = 10) -> list:
    posts = client.subreddit(subreddit_name).top(limit=limit)
    urls = []

    for post in posts:
        if post.url.endswith('.jpg') or post.url.endswith('.png'):
            urls.append(post.url)
    return urls


def download_pic(pic_url: str, save_to: str) -> None:
    r = httpx.get(pic_url)
    filename = os.path.basename(pic_url)
    pic_path = os.path.join(save_to, filename)
    with open(pic_path, 'wb') as f:
        f.write(r.content)


def get_cat_subs_info() -> None:
    url = 'https://www.reddit.com/r/Catsubs/wiki/index/'
    client = create_reddit_client()
    s = HTMLSession()

    r = s.get(url)
    tables = r.html.find('table')
    links = [i for table in tables for i in table.absolute_links]
    titles = [link.strip('/').split('/')[-1] for link in links]

    data = {}

    for title in titles:
        try:
            subreddit = client.subreddit(title)
            data[title] = subreddit.subscribers
        except Forbidden:
            continue

    result = {k: v for k, v in sorted(data.items(), key=lambda i: -i[1])}

    with open('cat_subs_info.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)
