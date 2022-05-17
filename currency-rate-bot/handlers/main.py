import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import keyboards as kb
from utils import (
    get_rates,
    currency_symbols,
    format_currency_message,
    CURRENCIES,
)


async def start(message: types.Message):
    text = 'Актуальные курсы валют ЦБ РФ.'
    await message.answer(text, reply_markup=kb.get_main_keyboard())


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info(f'Cancelling state {repr(current_state)}')
    await state.finish()
    await message.answer(
        'Операция отменена.', reply_markup=kb.get_main_keyboard()
    )


async def show_all_currencies(message: types.Message):
    await message.answer(
        'Все курсы валют ЦБ РФ.', reply_markup=kb.get_all_currencies_keyboard()
    )


async def get_usd_eur(message: types.Message):
    rate_data = await get_rates()
    currency_code = message.text
    currency_rate = rate_data[currency_code]
    text = await format_currency_message(currency_code, currency_rate)
    await message.answer(text)


async def get_rate(callback: types.CallbackQuery):
    rate_data = await get_rates()
    currency_code = callback.data
    currency_rate = rate_data[currency_code]
    text = await format_currency_message(currency_code, currency_rate)
    await callback.message.answer(text)
    await callback.answer()


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(cancel, commands='cancel', state='*')
    dp.register_message_handler(cancel, Text(equals='Отмена'), state='*')
    dp.register_message_handler(show_all_currencies, Text(equals='Все валюты'))
    dp.register_message_handler(get_usd_eur, Text(equals=currency_symbols))
    dp.register_callback_query_handler(get_rate, Text(equals=CURRENCIES.keys()))
