import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards as kb
from utils import (
    format_date,
    format_date_message,
)

date_directions = ['Курс одной валюты', 'Курс всех доступных валют']
date_currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']


class DateStates(StatesGroup):
    direction = State()
    currency = State()
    date_one = State()
    date_two = State()


async def start_date_rates(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*date_directions + ['Отмена'])
    text = 'Найти курс одной или нескольких валют?'
    await message.answer(text, reply_markup=kb)
    await DateStates.direction.set()


async def handle_currencies():
    pass


async def handle_date(message: types.Message):
    date = ''

    try:
        date = format_date(message.text)
    except ValueError:
        await message.answer('Формат даты должен быть ДД.ММ.ГГГГ')
        return

    return date


async def handle_date_one(message: types.Message, state: FSMContext):
    date = await handle_date(message)
    await state.update_data(date_one=date)


async def handle_date_two(message: types.Message, state: FSMContext):
    date = await handle_date(message)
    await state.update_data(date_two=date)


async def direction_date(message: types.Message, state: FSMContext):
    if message.text not in date_directions:
        await message.answer('Выберите операцию на клавиатуре внизу.')
        return
    if message.text == date_directions[0]:
        await state.update_data(direction='one_curr')
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        kb.add(*date_currencies)
        await DateStates.next()
        await message.answer('Выберите валюту:', reply_markup=kb)
    else:
        await state.update_data(direction='all_curr')

    await DateStates.next()
    await message.answer('Выберите валюту:', reply_markup=kb)


def handle_date_result():
    pass


def register_date_handlers(dp: Dispatcher):
    dp.register_message_handler(start_date_rates, commands='date', state='*')
    dp.register_message_handler(
        start_date_rates, Text(equals='Курс на определённую дату'), state='*'
    )
