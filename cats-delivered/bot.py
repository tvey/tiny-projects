import asyncio
import os

import dotenv
import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def send_meow():
    await bot.send_message(CHAT_ID, 'Meow')


async def scheduler():
    aioschedule.every(3).seconds.do(send_meow)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
