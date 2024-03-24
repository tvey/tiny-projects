import asyncio
import os
import logging

import dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import xkcd_base as xkcd
from telebot import types

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

bot = AsyncTeleBot(API_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['help', 'start'])
async def reply_on_start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('Comic!'))
    await bot.reply_to(
        message,
        xkcd.HELP_TEXT,
        reply_markup=kb,
        disable_web_page_preview=True,
    )


async def send_comic(message, latest=False):
    comic = await xkcd.get_comic(latest=latest)
    explain_btn = InlineKeyboardButton('Explain', callback_data=comic['id'])
    explain_kb = InlineKeyboardMarkup().add(explain_btn)
    logger.debug(f'Callback data: {comic["id"]}')

    await bot.send_photo(
        message.from_user.id,
        comic.get('bytes'),
        caption=f"<b>{comic['id']}. {comic['name']}</b>\n{comic['alt']}",
        reply_markup=explain_kb,
    )


@bot.message_handler(func=lambda message: 'comic' in message.text.lower())
async def get_comic(message):
    await send_comic(message)


@bot.message_handler(commands=['latest'])
async def get_latest(message):
    await send_comic(message, latest=True)


@bot.callback_query_handler(func=lambda call: True)
async def explain_comic(call):
    comic_id = call.data
    explanation = await xkcd.explain(comic_id)
    logger.debug(f'Explanation fetched for {comic_id}: {len(explanation)}')
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, explanation)


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, f'{message.text}? 😊')


if __name__ == '__main__':
    asyncio.run(bot.polling(skip_pending=True))
