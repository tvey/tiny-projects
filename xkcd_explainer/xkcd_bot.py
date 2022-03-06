import os
import logging
import json

import dotenv
from aiogram import Bot, Dispatcher, executor, types

import xkcd_base as xkcd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def reply_on_start(message: types.Message):
    text = 'Hi! I can send you a random /comic.'
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('Comic!'))
    await message.reply(text, reply_markup=kb)


@dp.message_handler(lambda message: 'comic' in message.text.lower())
async def get_comic(message: types.Message):
    comic = await xkcd.get_comic()
    explain_btn = types.InlineKeyboardButton(
        'Explain', callback_data=comic['id']
    )
    explain_kb = types.InlineKeyboardMarkup().add(explain_btn)

    await bot.send_photo(
        message.from_user.id,
        comic.get('bytes'),
        caption=f"<b>{comic['id']}. {comic['name']}</b>\n{comic['alt']}",
        reply_markup=explain_kb,
    )


@dp.message_handler(commands=['latest'])
async def get_latest(message: types.Message):
    comic = await xkcd.get_comic(latest=True)
    await bot.send_photo(
        message.from_user.id,
        comic.get('bytes'),
        caption=f"<b>{comic.get('id')}. {comic['name']}</b>\n{comic['alt']}",
    )


@dp.callback_query_handler()
async def explain(callback_query: types.CallbackQuery):
    explanation = await xkcd.explain(callback_query.data)
    await callback_query.answer()
    await callback_query.message.answer(explanation)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.text}? 😊')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
