from typing import Any, Dict

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import get_main_keyboard
from utils import (
    date_directions,
    currencies,
    currency_codes,
    verify_date,
    format_date,
    format_date_message,
)

directions = ['Курс одной валюты', 'Курс всех доступных валют']


class DateStates(StatesGroup):
    direction = State()
    currency = State()
    date_one = State()
    date_two = State()


async def start_date_rates(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*directions + ['Отмена'])
    text = 'Найти курс одной или нескольких валют?'
    await message.answer(text, reply_markup=kb)
    await DateStates.direction.set()


async def handle_direction(message: types.Message, state: FSMContext):
    if message.text not in directions:
        await message.answer('Выберите операцию на клавиатуре внизу.')
        return
    if message.text == directions[0]:
        await state.update_data(direction=date_directions[0])
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        kb.add(*currencies + ['Отмена'])
        await DateStates.next()
        await message.answer('Выберите валюту:', reply_markup=kb)
    else:
        await state.update_data(direction=date_directions[1])
        await DateStates.date_one.set()
        await message.answer(
            'Введите дату в формате ДД.ММ.ГГГГ:',
            reply_markup=types.ReplyKeyboardRemove(),
        )


async def handle_currency(message: types.Message, state: FSMContext):
    if message.text not in currencies:
        text = 'Выберите валюту из тех, что представлены ниже.'
        await message.answer(text)
        return
    currency_index = currencies.index(message.text)
    await state.update_data(currency=currency_codes[currency_index])
    await DateStates.next()  # date_one
    await message.answer(
        'Введите начальную дату в формате ДД.ММ.ГГГГ:',
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def handle_date(message: types.Message):
    date = message.text

    try:
        verify_date(date)
    except ValueError as e:
        await message.answer(e)  #
        return

    return date


async def handle_all_currencies(message: types.Message, state: FSMContext):
    """Show result for all currencies."""
    date = await handle_date(message)

    if date:
        await state.update_data(date_one=date)

    state_data = await state.get_data()

    if state_data['direction'] == date_directions[1]:
        await show_result(message, state_data)
        await state.finish()


async def handle_dates(message: types.Message, state: FSMContext):
    date = await handle_date(message)
    current_data = await state.get_data()

    if date and current_data['direction'] == date_directions[0]:
        await state.update_data(date_one=date)
    await DateStates.next()  # date_two
    await message.answer(
        'Введите дату окончания в формате ДД.ММ.ГГГГ или повторите начальную:',
    )


async def handle_one_currency(message: types.Message, state: FSMContext):
    """Show result for one currency."""
    date_two = await handle_date(message)

    if date_two:
        await state.update_data(date_two=date_two)

    state_data = await state.get_data()

    await show_result(message, state_data)
    await state.finish()


async def show_result(message: types.Message, state_data: Dict):
    direction = state_data.get('direction')

    if direction == date_directions[0]:
        currency_index = currencies.index(state_data.get('currency'))
        currency_code = currency_codes[currency_index]
        date_one = state_data.get('date_one')
        date_two = state_data.get('date_two')
        text = await format_date_message(
            direction, date_one, currency_code=currency_code, date_two=date_two
        )

    elif direction == date_directions[1]:
        date = state_data.get('date_one')
        text = await format_date_message(direction, date)

    await message.answer(text=text, reply_markup=get_main_keyboard())


def register_date_handlers(dp: Dispatcher):
    dp.register_message_handler(start_date_rates, commands='date', state='*')
    dp.register_message_handler(
        start_date_rates, Text(equals='Курс на определённую дату'), state='*'
    )
    dp.register_message_handler(handle_direction, state=DateStates.direction)
    dp.register_message_handler(handle_currency, state=DateStates.currency)
    dp.register_message_handler(
        handle_all_currencies, state=DateStates.date_one
    )
    dp.register_message_handler(handle_dates, state=DateStates.date_one)
    dp.register_message_handler(handle_one_currency, state=DateStates.date_two)
