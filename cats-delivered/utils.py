import os

import dotenv
import httpx
from praw import Reddit

dotenv.load_dotenv()

subreddits = [
    'cats',
    'catpics',
    'kitten',
    'Catloaf',
    'CatsStandingUp',
    'scrungycats',
    'Blep',
]


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


if __name__ == '__main__':
    client = create_reddit_client()
    all_subreddits = '+'.join(subreddits)
    pic_urls = get_pic_urls(client, all_subreddits)

    for url in pic_urls:
        download_pic(url, 'img')
