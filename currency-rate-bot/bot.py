import os

import dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from utils import get_rates, CURRENCIES

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

CURRENCY_CODES = [c['code'] for c in CURRENCIES]


@dp.message_handler(commands=['start'])
async def reply_on_start(message: types.Message):
    text = 'Актуальные курсы валют ЦБ РФ.'
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*['$', '€', 'Все валюты'])
    await message.reply(text, reply_markup=kb)


@dp.message_handler(Text(equals='Все валюты'))
async def display_all_currencies(message: types.Message):
    text = 'Все курсы валют ЦБ РФ.'
    kb = types.InlineKeyboardMarkup(row_width=1)
    currency_buttons = [
        types.InlineKeyboardButton(
            text=f'{c["nominal"]} {c["name"]}', callback_data=c['code']
        )
        for c in CURRENCIES
    ]
    kb.add(*currency_buttons)
    await message.answer(text, reply_markup=kb)


@dp.message_handler()
async def get_usd_eur(message: types.Message):
    rate_data = await get_rates()
    await message.answer(rate_data[message.text])


@dp.callback_query_handler()
async def get_rate(callback: types.CallbackQuery):
    rate_data = await get_rates()
    await callback.message.answer(rate_data[callback.data])
    await callback.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
