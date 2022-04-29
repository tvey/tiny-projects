from aiogram import types

from utils import CURRENCIES


def get_main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(*['$', '€'])
    kb.row('Все валюты')
    kb.row('Калькулятор')
    kb.row('Курс на определённую дату')
    return kb


def get_all_currencies_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    currency_buttons = [
        types.InlineKeyboardButton(
            text=f"{v['nominal']} {v['name']}", callback_data=k
        )
        for k, v in CURRENCIES.items()
    ]
    kb.add(*currency_buttons)

    return kb
