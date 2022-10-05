from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import get_main_keyboard
from utils import (
    calculate,
    selected_currencies,
    CURRENCIES,
    format_number,
)

directions = ['Из валюты в рубли', 'Из рублей в валюту']


class CalcStates(StatesGroup):
    direction = State()
    currency = State()
    amount = State()


async def start_calculator(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*directions + ['Отмена'])
    await message.answer('Как посчитать?', reply_markup=kb)
    await CalcStates.direction.set()


async def direction_currency(message: types.Message, state: FSMContext):
    if message.text not in directions:
        text = 'Пожалуйста, выберите направление, используя клавиатуру ниже.'
        await message.answer(text)
        return
    if message.text == directions[0]:
        await state.update_data(direction='to_rub')
    else:
        await state.update_data(direction='from_rub')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(*list(selected_currencies.keys()) + ['Отмена'])

    await CalcStates.next()
    await message.answer('Выберите валюту:', reply_markup=kb)


async def currency_amount(message: types.Message, state: FSMContext):
    if message.text not in selected_currencies.keys():
        await message.answer('Выберите валюту из тех, что представлены ниже.')
        return
    await state.update_data(currency=selected_currencies.get(message.text))

    await CalcStates.next()

    current_state = await state.get_data()
    direction = current_state.get('direction')
    msg = 'Введите сумму:'

    if direction == 'to_rub':
        msg = 'Введите сумму в валюте:'
    elif direction == 'from_rub':
        msg = 'Введите сумму в рублях:'

    await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())


async def calc_result(message: types.Message, state: FSMContext):
    amount = 0
    try:
        amount = float(message.text)
        if amount < 0:
            await message.answer('Введите положительное число, пожалуйста.')
            return
    except ValueError:
        await message.answer('Введите сумму цифрами.')
        return
    await state.update_data(amount=amount)

    user_data = await state.get_data()
    currency_id = user_data['currency']

    result = await calculate(
        user_data['direction'], currency_id, user_data['amount']
    )

    f_amount = format_number(user_data['amount'])
    f_result = format_number(result)

    if user_data['direction'] == 'from_rub':
        text = f"{f_amount} RUB = {f_result} {CURRENCIES[currency_id]['code']}"
    elif user_data['direction'] == 'to_rub':
        text = f"{f_amount} {CURRENCIES[currency_id]['code']} = {f_result} RUB"

    await message.answer(text, reply_markup=get_main_keyboard())
    await state.finish()


def register_calculator_handlers(dp: Dispatcher):
    dp.register_message_handler(start_calculator, commands='calc', state='*')
    dp.register_message_handler(
        start_calculator, Text(equals='Калькулятор'), state='*'
    )
    dp.register_message_handler(direction_currency, state=CalcStates.direction)
    dp.register_message_handler(currency_amount, state=CalcStates.currency)
    dp.register_message_handler(calc_result, state=CalcStates.amount)
