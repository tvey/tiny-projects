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

CURRENCIES['$'] = CURRENCIES['R01235']
CURRENCIES['€'] = CURRENCIES['R01239']

current_currencies = {k: v for k, v in CURRENCIES.items() if v['is_current']}
selected_currencies = ['Доллар', 'Евро', 'Юань', '', '', '']
selected_currency_ids = ['R01235', 'R01239', 'R01375', '', '', '']
currency_symbols = ['$', '€']
date_directions = ['one_currency', 'all_currencies']


async def get_rates(date: str = '', extra: bool = False) -> dict:
    """Get rates for available currencies for the current or historical date."""
    params = {'date_req': format_date(date)} if date else {}

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {
        i.get('@ID'): {'value': i.get('Value'), 'nominal': i.get('Nominal')}
        for i in data
    }

    if extra:
        return rates | {'$': rates['R01235'], '€': rates['R01239']}

    return rates


async def get_dynamic_rates(
    cbr_id: str, date_one: str, date_two: str = ''
) -> list:
    """Get rates for one currency for one date or a specified date span."""
    params = {
        'date_req1': format_date(date_one),
        'date_req2': format_date(date_one),
        'VAL_NM_RQ': cbr_id,
    }

    if date_two:
        params['date_req2'] = format_date(date_two)

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DYNAMIC, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Record']

    if isinstance(data, OrderedDict):
        data = [data]

    return [
        {'date': i['@Date'], 'nominal': i['Nominal'], 'value': i['Value']}
        for i in data
    ]


def get_current_date() -> datetime.date:
    return datetime.datetime.now(pytz.timezone('Europe/Moscow')).date()


def get_date_difference(date_one: str, date_two: str) -> int:
    former = datetime.datetime.strptime(date_one, '%d.%m.%Y').date()
    latter = datetime.datetime.strptime(date_two, '%d.%m.%Y').date()

    if latter < former:
        raise ValueError('Date two must be later than date one.')

    return (latter - former).days


def format_date(date: str) -> str:
    """Format a date string for use in a URL parameter."""
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%d/%m/%Y')


def verify_date(date_value: str, date_one: str = '') -> bool:
    initial_date = datetime.date(1992, 7, 1)
    current_date = get_current_date()

    try:
        date = datetime.datetime.strptime(date_value, '%d.%m.%Y').date()
    except ValueError as e:
        raise ValueError('Пожалуйста, введите правильную дату.')

    if date_one:
        previous_date = datetime.datetime.strptime(date_one, '%d.%m.%Y').date()
        if date < previous_date:
            raise ValueError(
                'Вторая дата не может быть раньше предыдущей. Попробуйте снова.'
            )       


    if date < initial_date:
        raise ValueError(
            'Дата должна быть не ранее 01.07.1992. Попробуйте снова.'
        )
    if date > current_date:
        raise ValueError(
            'Дата не может быть позднее текущей даты. Попробуйте снова.'
        )

    id 

    return True


def get_currency_str(cbr_id: str, nominal: int) -> str:
    currency = CURRENCIES.get(cbr_id)
    is_current = currency['is_current']
    redenominated = currency['redenominated']

    if is_current and not redenominated:
        name = currency.get('name')
    elif (not is_current or redenominated) and int(nominal) == 1:
        name = currency.get('name_singular')
    elif (not is_current or redenominated) and int(nominal) > 1:
        name = currency.get('name_plural')

    return f'{nominal} {name}'


async def calculate(direction: str, cbr_id: str, amount: float) -> float:
    rates = await get_rates()
    currency_rate = float(rates[cbr_id]['value'].replace(',', '.'))
    nominal = int(CURRENCIES[cbr_id]['nominal'])
    result = 0

    if direction == 'from_rub':
        result = amount / currency_rate * nominal
    elif direction == 'to_rub':
        result = amount * currency_rate / nominal
    return round(result, 4)


def format_number(value: int) -> str:
    return f'{value:,}'.replace(',', '\u2009').replace('.', ',')


async def format_currency_message(cbr_id: str, currency_rate: str) -> str:
    currency = CURRENCIES.get(cbr_id)
    if not currency:
        return ''
    return f"{currency['nominal']} {currency['name']} = {currency_rate} рублей"


async def format_date_message(
    direction: str, date_one: str, date_two: str = '', cbr_id: str = ''
) -> str:
    intro = ''
    body = ''

    if direction == date_directions[0]:
        if cbr_id and date_two:
            rates = await get_dynamic_rates(cbr_id, date_one, date_two=date_two)
            nom = rates[0]['nominal']  # !
            intro = f'{get_currency_str(cbr_id, nom)} (с {date_one} по {date_two}):'
        else:
            rates = await get_dynamic_rates(cbr_id, date_one)
            nom = rates[0]['nominal']  # !
            intro = f'{get_currency_str(cbr_id, nom)} на {date_one}:'

        body = '\n'.join([f"{i['date']}: {i['value']}" for i in rates])

    elif direction == date_directions[1]:
        intro = f'Курсы валют на {date_one}:'
        rates = await get_rates(date=date_one)
        rows = []
        for k, v in rates.items():
            nominal, value = v['nominal'], v['value']
            row = f'{get_currency_str(k, nominal)}: {value}'
            rows.append(row)
        body = '\n'.join(rows)

    return '\n'.join([intro, body])
