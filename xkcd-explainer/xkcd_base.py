import logging
import os
import random
import re

from aiohttp_client_cache import CachedSession, SQLiteBackend
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('xkcd_base.log'), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

for p in ['asyncio', 'aiogram', 'aiosqlite', 'aiohttp_client_cache']:
    logging.getLogger(p).setLevel(logging.WARNING)

XKCD_BASE = 'https://xkcd.com/'
XKCD_INFO = 'https://xkcd.com/{}/info.0.json'
EXPLAIN_BASE = 'https://www.explainxkcd.com/wiki/index.php/'
IRREGULAR_COMICS = [404, 961, 1037, 1116, 1264, 1350, 1416, 1608, 1663, 2198]
HELP_TEXT = (
    'Hey! I\'m bot that can send you random comic from '
    '<a href="https://xkcd.com/">xkcd.com</a> and fetch their explanations '
    'from <a href="https://explainxkcd.com/">explainxkcd.com</a>.'
    'Yep, sometimes you\'ll really want the explanations, '
    'and nope, it\'s not because you\'re dumb.'
)


async def get_latest_comic_id(session: CachedSession) -> int:
    async with session.get(XKCD_BASE) as r:
        html = await r.text()
        soup = BeautifulSoup(html, 'html.parser')
        prev_link = soup.select('.comicNav > li:nth-child(2) > a')[0]
        prev = prev_link.attrs['href'].strip('/')
        latest = int(prev) + 1
        logger.debug(f'Latest comic: {latest}')
        return latest


async def get_random_comic_id(latest_comic_id: int) -> int:
    random_id = random.randrange(1, latest_comic_id + 1)
    if random_id in IRREGULAR_COMICS:
        random_id = random.randrange(1, latest_comic_id + 1)
    logger.debug(f'Random comic id: {random_id}')
    return random_id


async def explain(comic_id):
    cache = SQLiteBackend(cache_name='xkcd', expire_after=-1)
    session = CachedSession(cache=cache)
    explink = f'{EXPLAIN_BASE}{comic_id}'

    r = await session.get(explink)
    page = await r.text()
    logger.debug(f'Explanation page size: {len(page)}')
    await session.close()

    expl_pattern = re.compile(
        r'(<h2><span class="mw-headline" id="Explanation">Explanation.+?<\/h2>)([\w\W]+?)<h2>'
    )
    match = expl_pattern.search(page)
    if match:
        raw_explanation = match.group(2)
        soup = BeautifulSoup(raw_explanation, 'html.parser')
        explanation = soup.get_text().replace('\n', '\n\n').lstrip()
        logger.debug(f'Explanation: {explanation[:100]}')
        return (
            f'<b>Explaining {comic_id}:</b>\n{explanation[:1000]}...\n{explink}'
        )
    return f'Comic {comic_id} is unexplainable!'


async def get_comic(latest=False):
    cache = SQLiteBackend(cache_name='xkcd', expire_after=60 * 60 * 24)
    session = CachedSession(cache=cache)
    latest_comic_id = await get_latest_comic_id(session)

    if latest:
        comic_id = latest_comic_id
    else:
        comic_id = await get_random_comic_id(latest_comic_id)
    comic_info_url = XKCD_INFO.format(comic_id)

    r = await session.get(comic_info_url)
    info = await r.json()

    comic_url = info.get('img')
    comic_url_2x = '_2x'.join(os.path.splitext(comic_url))

    r = await session.get(comic_url_2x)
    if r.status != 200:
        r = await session.get(comic_url)
    comic_bytes = await r.read()

    await session.close()

    comic = {
        'id': comic_id,
        'bytes': comic_bytes,
        'name': info.get('safe_title'),
        'alt': info.get('alt'),
    }
    logger.debug(f"Fetched data for {comic_id}: image - {bool(comic['bytes'])}")

    return comic
