import os
from io import BytesIO

import dotenv
import httpx
from asyncpraw import Reddit

dotenv.load_dotenv()


def create_reddit_client():
    return Reddit(
        client_id=os.environ.get('CLIENT_ID'),
        client_secret=os.environ.get('CLIENT_SECRET'),
        user_agent=os.environ.get('USER_AGENT'),
    )


async def get_image(subreddit_name: str = 'catloaf'):
    reddit = create_reddit_client()
    while True:
        subreddit = await reddit.subreddit(subreddit_name, fetch=True)
        submission = await subreddit.random()
        image_url = submission.url
        if not 'i.redd.it' in image_url:
            continue
        async with httpx.AsyncClient() as client:
            r = await client.get(image_url)
            return BytesIO(r.content)
