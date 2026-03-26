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


main_keyboard = ReplyKeyboardMarkup(
    [["Дай слова"], ["Привередливее"]], resize_keyboard=True
)


async def hey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Что хочешь?", reply_markup=main_keyboard)


async def just_give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("update.message.text", update.message.text)
    print("context.user_data", context.user_data)
    data = context.user_data
    count = data.get("count", 10)
    mode = data.get("mode", "Микс")
    words = generate_words(count=count, mode=mode)
    await update.message.reply_text("\n".join(words))


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
        await update.message.reply_text("Выбирай", reply_markup=main_keyboard)
        return

    count = int(text)
    context.user_data["count"] = count
    keyboard = [["Р"], ["Рь"], ["Микс"], ["Назад"]]

    await update.message.reply_text(
        "Какие?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Назад":
        await be_picky(update, context)
        return

    context.user_data["mode"] = text
    count = context.user_data.get("count", 10)
    mode = context.user_data.get("mode", "микс")
    words = generate_words(count=count, mode=mode)
    await update.message.reply_text("\n".join(words), reply_markup=main_keyboard)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Сброшено", reply_markup=main_keyboard)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hey", hey))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.Text("Дай слова"), just_give))
    app.add_handler(MessageHandler(filters.Text("Привередливее"), be_picky))
    app.add_handler(MessageHandler(filters.Regex(r"^\d+$|^Назад$"), choose_count))
    app.add_handler(MessageHandler(filters.Regex(r"^(Р|Рь|Микс|Назад)$"), choose_type))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
