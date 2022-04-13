import os

import dotenv
from aiogram import Bot, Dispatcher, executor, types

from utils import get_rates

dotenv.load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def reply_on_start(message: types.Message):
    text = 'Актуальные курсы доллара и евро.'
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*['$', '€'])
    await message.reply(text, reply_markup=kb)


@dp.message_handler()
async def get_rate(message: types.Message):
    rate_data = await get_rates()
    await message.reply(rate_data[message.text])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
