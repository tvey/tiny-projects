import asyncio
import os
import random

import dotenv
import aioschedule
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
IMAGE_FOLDER = 'img'

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def send_pic():
    pics = os.listdir(IMAGE_FOLDER)
    random_pic_path = os.path.join(IMAGE_FOLDER, random.choice(pics))
    pic_file = types.InputFile(random_pic_path)
    await bot.send_photo(CHAT_ID, photo=pic_file)


async def scheduler():
    aioschedule.every(1).hours.do(send_pic)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
