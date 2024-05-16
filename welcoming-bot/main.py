import asyncio
import logging
import os

import dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.types.chat_member_updated import ChatMemberUpdated
# from aiogram.utils.formatting import Url

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)
router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    chat = event.chat
    title = chat.title
    username = user.username
    msg = f'Welcome, {username}\\!'

    if title:
        msg = f'Welcome to [{title}](https://t.me/{chat.username}), {username}\\!'

    # This message will be sent to a private chat from the bot to the user
    await bot.send_message(user.id, msg, parse_mode=ParseMode.MARKDOWN_V2)

    # This message will be sent to a channel/group
    # which a user joined and where the bot is admin
    await event.answer(f'Glad to see you, {username}!' )


async def main() -> None:
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
