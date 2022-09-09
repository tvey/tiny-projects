from datetime import datetime

import httpx
import xmltodict

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

currency_symbols = ['$', '€']

CURRENCIES = {
    'AUD': {
        'cbr_id': 'R01010',
        'name': 'австралийский доллар',
        'nominal': '1',
    },
    'AZN': {
        'cbr_id': 'R01020A',
        'name': 'азербайджанский манат',
        'nominal': '1',
    },
    'GBP': {
        'cbr_id': 'R01035',
        'name': 'фунт стерлингов',
        'nominal': '1',
    },
    'AMD': {
        'cbr_id': 'R01060',
        'name': 'армянских драмов',
        'nominal': '100',
    },
    'BYN': {
        'cbr_id': 'R01090B',
        'name': 'белорусский рубль',
        'nominal': '1',
    },
    'BGN': {
        'cbr_id': 'R01100',
        'name': 'болгарский лев',
        'nominal': '1',
    },
    'BRL': {
        'cbr_id': 'R01115',
        'name': 'бразильский реал',
        'nominal': '1',
    },
    'HUF': {
        'cbr_id': 'R01135',
        'name': 'венгерских форинтов',
        'nominal': '100',
    },
    'HKD': {
        'cbr_id': 'R01200',
        'name': 'гонконгских долларов',
        'nominal': '10',
    },
    'DKK': {
        'cbr_id': 'R01215',
        'name': 'датская крона',
        'nominal': '1',
    },
    'USD': {
        'cbr_id': 'R01235',
        'name': 'доллар США',
        'nominal': '1',
    },
    'EUR': {
        'cbr_id': 'R01239',
        'name': 'евро',
        'nominal': '1',
    },
    'INR': {
        'cbr_id': 'R01270',
        'name': 'индийских рупий',
        'nominal': '100',
    },
    'KZT': {
        'cbr_id': 'R01335',
        'name': 'казахстанских тенге',
        'nominal': '100',
    },
    'CAD': {
        'cbr_id': 'R01350',
        'name': 'канадский доллар',
        'nominal': '1',
    },
    'KGS': {
        'cbr_id': 'R01370',
        'name': 'киргизских сомов',
        'nominal': '100',
    },
    'CNY': {
        'cbr_id': 'R01375',
        'name': 'китайский юань',
        'nominal': '1',
    },
    'MDL': {
        'cbr_id': 'R01500',
        'name': 'молдавских леев',
        'nominal': '10',
    },
    'NOK': {
        'cbr_id': 'R01535',
        'name': 'норвежских крон',
        'nominal': '10',
    },
    'PLN': {
        'cbr_id': 'R01565',
        'name': 'польский злотый',
        'nominal': '1',
    },
    'RON': {
        'cbr_id': 'R01585F',
        'name': 'румынский лей',
        'nominal': '1',
    },
    'XDR': {
        'cbr_id': 'R01589',
        'name': 'СДР',
        'nominal': '1',
    },
    'SGD': {
        'cbr_id': 'R01625',
        'name': 'сингапурский доллар',
        'nominal': '1',
    },
    'TJS': {
        'cbr_id': 'R01670',
        'name': 'таджикских сомони',
        'nominal': '10',
    },
    'TRY': {
        'cbr_id': 'R01700J',
        'name': 'турецких лир',
        'nominal': '10',
    },
    'TMT': {
        'cbr_id': 'R01710A',
        'name': 'туркменский манат',
        'nominal': '1',
    },
    'UZS': {
        'cbr_id': 'R01717',
        'name': 'узбекских сумов',
        'nominal': '10000',
    },
    'UAH': {
        'cbr_id': 'R01720',
        'name': 'украинских гривен',
        'nominal': '10',
    },
    'CZK': {
        'cbr_id': 'R01760',
        'name': 'чешских крон',
        'nominal': '10',
    },
    'SEK': {
        'cbr_id': 'R01770',
        'name': 'шведских крон',
        'nominal': '10',
    },
    'CHF': {
        'cbr_id': 'R01775',
        'name': 'швейцарский франк',
        'nominal': '1',
    },
    'ZAR': {
        'cbr_id': 'R01810',
        'name': 'южноафриканских рэндов',
        'nominal': '10',
    },
    'KRW': {
        'cbr_id': 'R01815',
        'name': 'вон Республики Корея',
        'nominal': '1000',
    },
    'JPY': {
        'cbr_id': 'R01820',
        'name': 'японских иен',
        'nominal': '100',
    },
}

CURRENCIES['$'] = CURRENCIES['USD']
CURRENCIES['€'] = CURRENCIES['EUR']

currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']
date_directions = ['one_currency', 'all_currencies']


async def get_rates(date: str = '', extra: bool = False):
    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params={'date_req': date})

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    if extra:
        return rates | {'$': rates['USD'], '€': rates['EUR']}

    return rates


async def get_dynamic_rates(curr_code: str, date_one: str, date_two: str = ''):
    cbr_id = CURRENCIES[curr_code]['cbr_id']
    params = {
        'date_req1': date_one,
        'date_req2': date_one,
        'VAL_NM_RQ': cbr_id,
    }
    if date_two:
        params['date_req2'] = date_two

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DYNAMIC, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Record']

    return [{'date': i['@Date'], 'value': i['Value']} for i in data]


def format_date(date_str):
    if '/' in date_str:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%d.%m.%Y')

    return datetime.strptime(date_str, '%d.%m.%Y').strftime('%d/%m/%Y')


def get_currency_str(currency_code):
    name = CURRENCIES[currency_code]['name']
    nominal = CURRENCIES[currency_code]['nominal']
    return f'{nominal} {name}'


async def calculate(direction, currency_code, amount):
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


async def format_currency_message(currency_code, currency_rate):
    if currency_code not in CURRENCIES.keys():
        return ''  #

    currency = CURRENCIES[currency_code]
    return f"{currency['nominal']} {currency['name']} = {currency_rate} рублей"


async def format_date_message(
    direction, date_one, date_two='', currency_code=''
):
    if direction == date_directions[0]:
        if currency_code and date_two:
            rates = await get_dynamic_rates(currency_code, date_one, date_two)
            intro = (
                f'{get_currency_str(currency_code)} с {date_one} по {date_two}:'
            )
        else:
            rates = await get_dynamic_rates(currency_code, date_one)
            intro = f'{get_currency_str(currency_code)} на {date_one}:'

        body = '\n'.join(
            [f"{format_date(i['date']): {i['value']}}" for i in rates]
        )

    elif direction == date_directions[1]:
        intro = f'Курсы валют на {format_date(date_one)}:'
        rates = await get_rates(date=date_one)
        rows = []
        for code, value in rates.items():
            row = f"{get_currency_str(code)}: {value}"
            rows.append(row)
        body = '\n'.join(rows)

    return '\n'.join([intro, body])


"""
!!!!
Неизвестные значения кода валюты - например, BYR - то есть нужно добавить в мой список

Найти границы дат - какая самая первая
И дата не должна быть позже сеглдняшней по Москве


"""
