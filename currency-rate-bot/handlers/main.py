from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import keyboards as kb
from utils import get_rates, CURRENCIES


async def start(message: types.Message):
    text = 'Актуальные курсы валют ЦБ РФ.'
    await message.answer(text, reply_markup=kb.get_main_keyboard())


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Операция отменена.', reply_markup=kb.get_main_keyboard()
    )


async def display_all_currencies(message: types.Message):
    await message.answer(
        'Все курсы валют ЦБ РФ.', reply_markup=kb.get_all_currencies_keyboard()
    )


async def get_usd_eur(message: types.Message):
    rate_data = await get_rates()
    await message.answer(rate_data[message.text])


async def get_rate(callback: types.CallbackQuery):
    rate_data = await get_rates()
    await callback.message.answer(rate_data[callback.data])
    await callback.answer()


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(cancel, commands='cancel', state='*')
    dp.register_message_handler(Text(equals='Отмена'), state='*')
    dp.register_message_handler(display_all_currencies, Text(equals='Все валюты'))
    dp.register_message_handler(get_usd_eur, Text(equals=CURRENCIES.keys()))
    dp.register_callback_query_handler(get_rate)
