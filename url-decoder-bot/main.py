import os
import urllib.parse

import dotenv
import idna
from idna.core import InvalidCodepoint
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


def process_link(value: str) -> str:
    domain = urllib.parse.urlsplit(value).netloc

    if domain:
        try:
            decoded_domain = idna.decode(domain)
            url = value.replace(domain, decoded_domain)
            return urllib.parse.unquote(url)
        except (UnicodeError, InvalidCodepoint):
            pass

    return urllib.parse.unquote(value)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to the /start command."""
    text = (
        "Hi! Here you can get a more readable version "
        "of a link that you copied from your browser's address bar."
    )
    await update.message.reply_text(text)


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Reply to the /help command."""
    text = 'Just send me a link that you want to make more readable.'
    await update.message.reply_text(text)


async def decode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a more readable version of a link if it was possible to create."""
    text = update.message.text
    result = process_link(text)
    await update.message.reply_text(result)


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, decode))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
