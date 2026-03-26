import os

import logging

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from utils import generate_words

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main_keyboard(user_data):
    buttons = [["Дай слова"], ["Привередливее"]]

    if user_data.get("count") or user_data.get("mode"):
        buttons.append(["Почистить настройки"])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_word_result(user_data) -> str:
    count = user_data.get("count", 10)
    mode = user_data.get("mode", "Микс")
    words = generate_words(count=count, mode=mode)
    return "\n".join(words)


async def hey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Что хочешь?", reply_markup=main_keyboard(context.user_data)
    )


async def just_give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_word_result(context.user_data))


async def be_picky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["10", "20", "30"],
        ["Назад"],
    ]
    await update.message.reply_text(
        "Сколько слов?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )


async def choose_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Назад":
        await update.message.reply_text(
            "Выбирай", reply_markup=main_keyboard(context.user_data)
        )
        return

    context.user_data["count"] = int(text)
    buttons = [["Р", "Рь", "Микс"], ["Назад"]]

    await update.message.reply_text(
        "Какие?",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True),
    )


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Назад":
        await be_picky(update, context)
        return

    context.user_data["mode"] = text
    await update.message.reply_text(
        get_word_result(context.user_data),
        reply_markup=main_keyboard(context.user_data),
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Сброшено", reply_markup=main_keyboard(context.user_data)
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hey", hey))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.Text("Дай слова"), just_give))
    app.add_handler(MessageHandler(filters.Text("Привередливее"), be_picky))
    app.add_handler(MessageHandler(filters.Text("Почистить настройки"), clear))
    app.add_handler(MessageHandler(filters.Regex(r"^\d+$|^Назад$"), choose_count))
    app.add_handler(MessageHandler(filters.Regex(r"^(Р|Рь|Микс|Назад)$"), choose_type))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
