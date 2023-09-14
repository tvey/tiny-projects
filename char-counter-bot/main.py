import os
import re

import dotenv
from string import whitespace
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


def get_count_result(text: str) -> str:
    chars = len(text)
    space_count = len([i for i in text if i in whitespace])
    chars_no_spaces = chars - space_count
    words = len(re.findall(r'\w+', text)) 

    return (
        'Your result:\n'
        f'Total characters: {chars}\n'
        f'Characters without spaces: {chars_no_spaces}\n'
        f'Words: {words}'
    ) 


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to the /start command."""
    text = "Hi! Send me your text, and I will count words and characters."
    await update.message.reply_text(text)


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Reply to the /help command."""
    text = 'Just send me your text for counting.'
    await update.message.reply_text(text)


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the result."""
    text = update.message.text
    result = get_count_result(text)
    await update.message.reply_text(result)


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
