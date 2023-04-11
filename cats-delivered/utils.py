import json
import os

import dotenv
import httpx
from praw import Reddit
from prawcore.exceptions import Forbidden
from requests_html import HTMLSession

dotenv.load_dotenv()

cat_subs = os.getenv('CAT_SUBS').split(', ')



def create_reddit_client() -> Reddit:
    client = Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        user_agent=os.environ.get('REDDIT_APP_NAME'),
    )
    return client


def get_image_urls(client: Reddit, subreddit_name: str, limit: int = 10) -> list:
    posts = client.subreddit(subreddit_name).top(limit=limit)
    urls = []

    for post in posts:
        if post.url.endswith('.jpg') or post.url.endswith('.png'):
            urls.append(post.url)
    return urls


def download_image(image_url: str, save_to: str) -> None:
    r = httpx.get(image_url)
    filename = os.path.basename(image_url)
    image_path = os.path.join(save_to, filename)
    with open(image_path, 'wb') as f:
        f.write(r.content)



