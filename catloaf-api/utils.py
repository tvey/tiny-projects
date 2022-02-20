import os

import dotenv
import requests
from praw import Reddit

dotenv.load_dotenv()


def create_reddit_client():
    return Reddit(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        user_agent=os.environ.get('APP_NAME'),
    )


def get_image(subreddit_name: str = 'catloaf'):
    reddit = create_reddit_client()
    while True:
        image_url = reddit.subreddit(subreddit_name).random().url
        if not image_url.endswith('.jpg'):
            continue
        return requests.get(image_url, stream=True).raw
