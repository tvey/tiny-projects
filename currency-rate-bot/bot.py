import os

import dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import get_rates, CURRENCIES

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


calc_directions = ['Из валюты в рубли', 'Из рублей в валюту']
calc_currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']


class CalculatorStates(StatesGroup):
    direction_state = State()
    currency_state = State()
    amount_state = State()


@dp.message_handler(commands=['start'])
async def reply_on_start(message: types.Message):
    text = 'Актуальные курсы валют ЦБ РФ.'
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(*['$', '€'])
    kb.row('Все валюты')
    kb.row('Калькулятор')
    await message.reply(text, reply_markup=kb)


@dp.message_handler(Text(equals='Все валюты'))
async def display_all_currencies(message: types.Message):
    text = 'Все курсы валют ЦБ РФ.'
    kb = types.InlineKeyboardMarkup(row_width=1)
    currency_buttons = [
        types.InlineKeyboardButton(
            text=f'{v["nominal"]} {v["name"]}', callback_data=k
        )
        for k, v in CURRENCIES.items()
    ]
    kb.add(*currency_buttons)
    await message.answer(text, reply_markup=kb)


@dp.message_handler()
async def get_usd_eur(message: types.Message):
    rate_data = await get_rates()
    await message.answer(rate_data[message.text])


@dp.callback_query_handler()
async def get_rate(callback: types.CallbackQuery):
    rate_data = await get_rates()
    await callback.message.answer(rate_data[callback.data])
    await callback.answer()


@dp.message_handler(commands=['Калькулятор'])
async def start_calculator(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*calc_directions)
    await message.answer('Как посчитать?', reply_markup=kb)
    await CalculatorStates.direction_state.set()


async def direction_currency(message: types.Message, state: FSMContext):
    if message.text not in calc_directions:
        text = 'Пожалуйста, выберите направление, используя клавиатуру ниже.'
        await message.answer(text)
        return
    if message.text == calc_currencies[0]:
        await state.update_data(direction=0)
    else:
        await state.update_data(direction=1)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*calc_currencies)

    await CalculatorStates.next()
    await message.answer('Выберите валюту:', reply_markup=kb)


async def currency_amount(message: types.Message, state: FSMContext):
    if message.text not in calc_currencies:
        text = 'Выберите валюту из тех, что представлены ниже.'
        await message.answer(text)
        return
    currency_index = calc_currencies.index(message.text)
    await state.update_data(direction=currency_codes[currency_index])

    await CalculatorStates.next()
    await message.answer('Введите сумму:')


async def result(message: types.Message, state: FSMContext):
    amount = 0
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer('Введите положительное число, пожалуйста.')  #
        return
    await state.update_data(amount=amount)

    user_state_data = await state.get_data()

    # calculate
    await message.answer()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
