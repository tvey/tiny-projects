import csv
import logging
import re
from dataclasses import dataclass

import nltk
from nltk.stem import WordNetLemmatizer
from pymorphy3 import MorphAnalyzer
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    MessageHandler,
    filters,
)

BOT_TOKEN = 'YOUR_BOT_TOKEN'
FILE = 'tg_data.csv'
KEYWORDS = {
    'python',
    'телеграм',
    'пример',
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

nltk.download('omw-1.4')
nltk.download('wordnet')
en_analyzer = WordNetLemmatizer()
ru_analyzer = MorphAnalyzer()


@dataclass
class Message:
    username: str
    user_id: int
    chat_id: int
    message: str
    timestamp: str


def normalize_text(text, language='en'):
    """Привести слова сообщения к нормальной форме."""
    table = str.maketrans('', '', ',.?!:;…')
    text = text.translate(table)  # убрать знаки препинания
    words = text.split()
    if language == 'en':
        return ' '.join(en_analyzer.lemmatize(word) for word in words)
    elif language == 'ru':
        return ' '.join(
            ru_analyzer.parse(word)[0].normal_form for word in words
        )
    return text


def save_to_csv(message: Message):
    """Сохранить поля сообщения в csv файл. Создать файл, если его нет."""
    fieldnames = ['username', 'user_id', 'chat_id', 'message', 'timestamp']

    with open(FILE, 'a', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(message.__dict__)


async def handle_message(update: Update, context: CallbackContext):
    message = update.message
    language = 'ru' if re.search('[\u0400-\u04FF]', message.text) else 'en'
    normalized_text = normalize_text(message.text, language)
    if any(keyword in normalized_text for keyword in KEYWORDS):
        message = Message(
            username=message.from_user.username,
            user_id=message.from_user.id,
            chat_id=message.chat_id,
            message=message.text,
            timestamp=message.date.isoformat(),  # UTC, назад: fromisoformat
        )
        save_to_csv(message)
        logger.info(f'Сохранено сообщение от: {message.from_user.username}')


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
