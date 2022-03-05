import logging
import os
import random
import re
from io import BytesIO

import aiohttp
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)

XKCD_BASE = 'https://xkcd.com/'
XKCD_EMBED_BASE = 'https://imgs.xkcd.com/comics/'
EXPLAIN_BASE = 'https://www.explainxkcd.com/wiki/index.php/'
IRREGULAR_COMICS = [404, 961, 1037, 1116, 1264, 1350, 1416, 1608, 1663, 2198]


async def get_latest_comic_num():
    async with aiohttp.ClientSession() as session:
        r = await session.get(XKCD_BASE)
        html = await r.text()
        soup = BeautifulSoup(html, 'html.parser')
        prev_link = soup.select('.comicNav > li:nth-child(2) > a')[0]
        prev = prev_link.attrs['href'].strip('/')
        latest = int(prev) + 1
        logging.debug(f'Latest comic: {latest}')
        return latest


async def get_random_comic_num():
    random_id = random.randrange(1, await get_latest_comic_num() + 1)
    if random_id in IRREGULAR_COMICS:
        random_id = random.randrange(1, await get_latest_comic_num() + 1)
    logging.debug(f'Random comic id: {random_id}')
    return random_id


async def explain(session, comic_num):
    explink = f'{EXPLAIN_BASE}{comic_num}'

    async with session.get(explink) as r:
        page = await r.text()

        expl_pattern = re.compile(
            r'(<h2><span class="mw-headline" id="Explanation">Explanation.+?<\/h2>)([\w\W]+?)<h2>'
        )
        expl_mess = expl_pattern.search(page).group(2)
        soup = BeautifulSoup(expl_mess, 'html.parser')
        explanation = soup.get_text().replace('\n', '\n\n').lstrip()
        if len(explanation) < 1000:
            return explanation + f'...\n{explink}'
        return explanation[:1000] + f'...\n{explink}'


async def get_comic():
    comic_num = await get_random_comic_num()
    session = aiohttp.ClientSession()

    async with session.get(f'{XKCD_BASE}{comic_num}') as r:
        page = await r.text()

    image_url_regex = re.compile(
        # Image URL (for hotlinking/embedding): <a href= "https://imgs.xkcd.com/comics/outlet_denier.png">
        r'Image URL \(for hotlinking\/embedding\): <a href= "(https:\/\/imgs\.xkcd\.com\/comics\/.+\.[jepng]{3,4})">'
    )
    match = re.search(image_url_regex, str(page))
    image_url = match.group(1)
    logging.debug(f'Image URL for {comic_num}: {image_url}')
    image_url_2x = '_2x'.join(os.path.splitext(image_url))

    soup = BeautifulSoup(page, 'html.parser')
    title = soup.select('#comic img')[0].get('title')

    async with session.get(image_url) as r:
        image_bytes = await r.content

    comic = {
        'comic_num': comic_num,
        'comic_bytes': BytesIO(image_bytes),
        'comic_title': title,
        'explanation': await explain(session, comic_num),
    }

    return comic
