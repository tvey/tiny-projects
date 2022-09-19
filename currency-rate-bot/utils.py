import datetime
import json
from collections import OrderedDict

import httpx
import pytz
import xmltodict

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

with open('currencies.json', encoding='utf-8') as f:
    CURRENCIES = json.load(f)

CURRENCIES['$'] = CURRENCIES['USD']
CURRENCIES['€'] = CURRENCIES['EUR']

current_currencies = {k: v for k, v in CURRENCIES.items() if v['is_current']}
selected_currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']
date_directions = ['one_currency', 'all_currencies']
currency_symbols = ['$', '€']


async def get_rates(date: str = '', extra: bool = False) -> dict:
    params = {'date_req': format_date(date)} if date else {}

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    if extra:
        return rates | {'$': rates['USD'], '€': rates['EUR']}

    return rates


async def get_dynamic_rates(
    curr_code: str, date_one: str, date_two: str = ''
) -> list:
    cbr_id = CURRENCIES[curr_code]['cbr_id']
    params = {
        'date_req1': format_date(date_one),
        'date_req2': format_date(date_one),
        'VAL_NM_RQ': cbr_id,
    }

    if date_two:
        params['date_req2'] = format_date(date_two)

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DYNAMIC, params=params)

    data = xmltodict.parse(r.content)

    data = xmltodict.parse(r.content)['ValCurs']['Record']

    if isinstance(data, OrderedDict):
        data = [data]

    return [{'date': i['@Date'], 'value': i['Value']} for i in data]


def get_current_date() -> datetime.date:
    return datetime.datetime.now(pytz.timezone('Europe/Moscow')).date()


def get_date_difference(date_one: str, date_two: str) -> int:
    former = datetime.datetime.strptime(date_one, '%d.%m.%Y').date()
    latter = datetime.datetime.strptime(date_two, '%d.%m.%Y').date()

    if latter < former:
        raise ValueError('Date two must be later than date one.')

    return (latter - former).days


def format_date(date: str) -> str:
    """Format a date string to use it as a URL parameter."""
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%d/%m/%Y')


def verify_date(date_value: str) -> bool:
    initial_date = datetime.date(1992, 7, 1)
    current_date = get_current_date()

    try:
        date = datetime.datetime.strptime(date_value, '%d.%m.%Y').date()
    except ValueError as e:
        raise ValueError('Пожалуйста, введите правильную дату.')

    if date < initial_date:
        raise ValueError(
            'Дата должна быть не ранее 01.07.1992. Попробуйте снова.'
        )
    if date > current_date:
        raise ValueError(
            'Дата не может быть позднее текущей даты. Попробуйте снова.'
        )

    return True


def get_currency_str(currency_code: str) -> str:
    name = CURRENCIES[currency_code]['name']
    nominal = CURRENCIES[currency_code]['nominal']
    return f'{nominal} {name}'


async def calculate(direction: str, currency_code: str, amount: float) -> float:
    rates = await get_rates()
    currency_rate = float(rates.get(currency_code).replace(',', '.'))
    nominal = int(CURRENCIES[currency_code]['nominal'])
    result = 0

    if direction == 'from_rub':
        result = amount / currency_rate * nominal
    elif direction == 'to_rub':
        result = amount * currency_rate / nominal
    return round(result, 4)


def format_number(value: int) -> str:
    return f'{value:,}'.replace(',', '\u2009').replace('.', ',')


async def format_currency_message(
    currency_code: str, currency_rate: str
) -> str:
    if currency_code not in CURRENCIES.keys():
        return ''  #

    currency = CURRENCIES[currency_code]
    return f"{currency['nominal']} {currency['name']} = {currency_rate} рублей"


async def format_date_message(
    direction: str, date_one: str, date_two: str = '', currency_code: str = ''
) -> str:
    intro = ''
    body = ''

    if direction == date_directions[0]:
        if currency_code and date_two:
            rates = await get_dynamic_rates(
                currency_code, date_one, date_two=date_two
            )
            intro = f'{get_currency_str(currency_code)} (с {date_one} по {date_two}):'
        else:
            rates = await get_dynamic_rates(currency_code, date_one)
            intro = f'{get_currency_str(currency_code)} на {date_one}:'

        body = '\n'.join([f"{i['date']}: {i['value']}" for i in rates])

    elif direction == date_directions[1]:
        intro = f'Курсы валют на {date_one}:'
        rates = await get_rates(date=date_one)
        rows = []
        for code, value in rates.items():
            row = f'{get_currency_str(code)}: {value}'
            rows.append(row)
        body = '\n'.join(rows)

    return '\n'.join([intro, body])
