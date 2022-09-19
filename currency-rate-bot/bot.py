import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.calculator import register_calculator_handlers
from handlers.date import register_date_handlers
from handlers.main import register_main_handlers

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/main', description='Показать главное меню'),
        BotCommand(command='/calc', description='Валютный калькулятор'),
        BotCommand(command='/date', description='Курсы на определённую дату'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    logger.info('Starting bot')

    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_main_handlers(dp)
    register_calculator_handlers(dp)
    register_date_handlers(dp)

    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
