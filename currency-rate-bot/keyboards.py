from aiogram import types

from utils import current_currencies, currency_symbols


def get_main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(*currency_symbols)
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
        for k, v in current_currencies.items() if k not in currency_symbols
    ]
    kb.add(*currency_buttons)

    return kb
