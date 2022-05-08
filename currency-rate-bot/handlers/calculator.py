from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards as kb
from utils import calculate

calc_directions = ['Из валюты в рубли', 'Из рублей в валюту']
calc_currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']


class CalcStates(StatesGroup):
    direction = State()
    currency = State()
    amount = State()


async def start_calculator(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(*calc_directions + ['Отмена'])
    await message.answer('Как посчитать?', reply_markup=kb)
    await CalcStates.direction.set()


async def direction_currency(message: types.Message, state: FSMContext):
    if message.text not in calc_directions:
        text = 'Пожалуйста, выберите направление, используя клавиатуру ниже.'
        await message.answer(text)
        return
    if message.text == calc_directions[0]:
        await state.update_data(direction='to_rub')
    else:
        await state.update_data(direction='from_rub')

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(*calc_currencies)

    await CalcStates.next()
    await message.answer('Выберите валюту:', reply_markup=kb)


async def currency_amount(message: types.Message, state: FSMContext):
    if message.text not in calc_currencies:
        text = 'Выберите валюту из тех, что представлены ниже.'
        await message.answer(text)
        return
    currency_index = calc_currencies.index(message.text)
    await state.update_data(currency=currency_codes[currency_index])

    await CalcStates.next()
    await message.answer(
        'Введите сумму:', reply_markup=types.ReplyKeyboardRemove()
    )


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

    result = await calculate(
        user_data['direction'], user_data['currency'], user_data['amount']
    )

    if user_data['direction'] == 'from_rub':
        text = f"{user_data['amount']} RUB = {result} {user_data['currency']}"
    elif user_data['direction'] == 'to_rub':
        text = f"{user_data['amount']} {user_data['currency']} = {result} RUB"

    await message.answer(text, reply_markup=kb.get_main_keyboard())
    await state.finish()


def register_calculator_handlers(dp: Dispatcher):
    dp.register_message_handler(start_calculator, commands='calc', state='*')
    dp.register_message_handler(start_calculator, Text(equals='Калькулятор'), state='*')
    dp.register_message_handler(direction_currency, state=CalcStates.direction)
    dp.register_message_handler(currency_amount, state=CalcStates.currency)
    dp.register_message_handler(calc_result, state=CalcStates.amount)
