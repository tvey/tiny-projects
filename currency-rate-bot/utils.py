import asyncio
import datetime
from collections import OrderedDict

import httpx
import pytz
import xmltodict

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

currency_symbols = ['$', '€']

CURRENCIES = {
    'AMD': {
        'cbr_id': 'R01060',
        'name': 'армянских драмов',
        'nominal': '100',
    },
    'ATS': {
        'cbr_id': 'R01015',
        'name': 'австрийских шиллингов',
        'nominal': '10',
    },
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
    'BEF': {
        'cbr_id': 'R01095',
        'name': 'бельгийских франков',
        'nominal': '100',
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
    'BYB': {
        'cbr_id': 'R01090A',
        'name': 'белoрусских рублей',
        'nominal': '1000000',
    },
    'BYN': {
        'cbr_id': 'R01090B',
        'name': 'белорусский рубль',
        'nominal': '1',
    },
    'BYR': {
        'cbr_id': 'R01090',
        'name': 'белорусских рублей',
        'nominal': '10000',
    },
    'CAD': {
        'cbr_id': 'R01350',
        'name': 'канадский доллар',
        'nominal': '1',
    },
    'CHF': {
        'cbr_id': 'R01775',
        'name': 'швейцарский франк',
        'nominal': '1',
    },
    'CNY': {
        'cbr_id': 'R01375',
        'name': 'китайский юань',
        'nominal': '1',
    },
    'CZK': {
        'cbr_id': 'R01760',
        'name': 'чешских крон',
        'nominal': '10',
    },
    'DEM': {
        'cbr_id': 'R01510',
        'name': 'немецкая марка',
        'nominal': '1',
    },
    'DKK': {
        'cbr_id': 'R01215',
        'name': 'датская крона',
        'nominal': '1',
    },
    'EEK': {
        'cbr_id': 'R01795',
        'name': 'эстонских крон',
        'nominal': '10',
    },
    'ESP': {
        'cbr_id': 'R01315',
        'name': 'испанских песет',
        'nominal': '100',
    },
    'EUR': {
        'cbr_id': 'R01239',
        'name': 'евро',
        'nominal': '1',
    },
    'FIM': {
        'cbr_id': 'R01740',
        'name': 'финляндских марок',
        'nominal': '10',
    },
    'FRF': {
        'cbr_id': 'R01750',
        'name': 'французских франков',
        'nominal': '10',
    },
    'GBP': {
        'cbr_id': 'R01035',
        'name': 'фунт стерлингов',
        'nominal': '1',
    },
    'GRD': {
        'cbr_id': 'R01205',
        'name': 'греческих драхм',
        'nominal': '1000',
    },
    'HKD': {
        'cbr_id': 'R01200',
        'name': 'гонконгских долларов',
        'nominal': '10',
    },
    'HUF': {
        'cbr_id': 'R01135',
        'name': 'венгерских форинтов',
        'nominal': '100',
    },
    'IEP': {
        'cbr_id': 'R01305',
        'name': 'ирландский фунт',
        'nominal': '1',
    },
    'INR': {
        'cbr_id': 'R01270',
        'name': 'индийских рупий',
        'nominal': '100',
    },
    'ISK': {
        'cbr_id': 'R01310',
        'name': 'исландских крон',
        'nominal': '100',
    },
    'ITL': {
        'cbr_id': 'R01325',
        'name': 'итальянских лир',
        'nominal': '1000',
    },
    'JPY': {
        'cbr_id': 'R01820',
        'name': 'японских иен',
        'nominal': '100',
    },
    'KGS': {
        'cbr_id': 'R01370',
        'name': 'киргизских сомов',
        'nominal': '100',
    },
    'KRW': {
        'cbr_id': 'R01815',
        'name': 'вон республики корея',
        'nominal': '1000',
    },
    'KZT': {
        'cbr_id': 'R01335',
        'name': 'казахстанских тенге',
        'nominal': '100',
    },
    'LTL': {
        'cbr_id': 'R01435',
        'name': 'литовский лит',
        'nominal': '1',
    },
    'LVL': {
        'cbr_id': 'R01405',
        'name': 'латвийский лат',
        'nominal': '1',
    },
    'MDL': {
        'cbr_id': 'R01500',
        'name': 'молдавских леев',
        'nominal': '10',
    },
    'NLG': {
        'cbr_id': 'R01523',
        'name': 'нидерландский гульден',
        'nominal': '1',
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
    'PTE': {
        'cbr_id': 'R01570',
        'name': 'португальских эскудо',
        'nominal': '100',
    },
    'RON': {
        'cbr_id': 'R01585F',
        'name': 'румынский лей',
        'nominal': '1',
    },
    'SEK': {
        'cbr_id': 'R01770',
        'name': 'шведских крон',
        'nominal': '10',
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
    'TMT': {
        'cbr_id': 'R01710A',
        'name': 'новый туркменский манат',
        'nominal': '1',
    },
    'TRL': {
        'cbr_id': 'R01700',
        'name': 'турецких лир',
        'nominal': '1000000',
    },
    'TRY': {
        'cbr_id': 'R01700J',
        'name': 'турецких лир',
        'nominal': '10',
    },
    'UAH': {
        'cbr_id': 'R01720',
        'name': 'украинских гривен',
        'nominal': '10',
    },
    'USD': {
        'cbr_id': 'R01235',
        'name': 'доллар сша',
        'nominal': '1',
    },
    'UZS': {
        'cbr_id': 'R01717',
        'name': 'узбекских сумов',
        'nominal': '10000',
    },
    'XDR': {
        'cbr_id': 'R01589',
        'name': 'СДР',
        'nominal': '1',
    },
    'XEU': {
        'cbr_id': 'R01790',
        'name': 'ЭКЮ',
        'nominal': '1',
    },
    'ZAR': {
        'cbr_id': 'R01810',
        'name': 'южноафриканских рэндов',
        'nominal': '10',
    }
}

CURRENCIES['$'] = CURRENCIES['USD']
CURRENCIES['€'] = CURRENCIES['EUR']

currencies = ['Доллар', 'Евро', 'Юань']
currency_codes = ['USD', 'EUR', 'CNY']
date_directions = ['one_currency', 'all_currencies']


async def get_rates(date: str = '', extra: bool = False):
    params = {'date_req': format_date(date)} if date else {}

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    if extra:
        return rates | {'$': rates['USD'], '€': rates['EUR']}

    return rates


async def get_dynamic_rates(curr_code: str, date_one: str, date_two: str = ''):
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


def get_current_date():
    return datetime.datetime.now(pytz.timezone('Europe/Moscow')).date()


def get_date_difference(date_one: str, date_two: str) -> int:
    former = datetime.datetime.strptime(date_one, '%d.%m.%Y').date()
    latter = datetime.datetime.strptime(date_two, '%d.%m.%Y').date()

    if latter < former:
        raise ValueError('Date two must be later than date one.')

    return (latter - former).days


def format_date(date: str) -> str:
    '''Format a date string to use it as a URL parameter.'''
    return datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%d/%m/%Y')


def verify_date(date_value: str) -> bool:
    initial_date = datetime.date(1992, 7, 1)
    current_date = get_current_date()

    try:
        date = datetime.datetime.strptime(date_value, '%d.%m.%Y').date()
    except ValueError as e:
        raise ValueError('Пожалуйста, введите правильную дату.')

    if date < initial_date:
        raise ValueError('Дата должна быть не ранее 01.07.1992.')

    if date > current_date:
        raise ValueError('Дата не может быть позднее текущей даты.')

    return True


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
    intro = ''
    body = ''
    if direction == date_directions[0]:
        if currency_code and date_two:
            rates = await get_dynamic_rates(currency_code, date_one, date_two)
            intro = (
                f'{get_currency_str(currency_code)} с {date_one} по {date_two}:'
            )
        else:
            rates = await get_dynamic_rates(currency_code, date_one)
            intro = f'{get_currency_str(currency_code)} на {date_one}:'

        body = '\n'.join([f'{i['date']: {i['value']}}' for i in rates])

    elif direction == date_directions[1]:
        intro = f'Курсы валют на {date_one}:'
        rates = await get_rates(date=date_one)
        rows = []
        for code, value in rates.items():
            row = f'{get_currency_str(code)}: {value}'
            rows.append(row)
        body = '\n'.join(rows)

    return '\n'.join([intro, body])





async def get_historical_currencies_info(date):
    await asyncio.sleep(2)

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params={'date_req': format_date(date)})

    if xmltodict.parse(r.content).get('ValCurs'):
        if xmltodict.parse(r.content).get('ValCurs').get('Valute'):

            data = xmltodict.parse(r.content)['ValCurs']['Valute']
            try:
                elems = [
                    {
                        'cbr_id': i.get('@ID'),
                        'code': i.get('CharCode'),
                        'name': i.get('Name'),
                        'nominal': i.get('Nominal'),
                    }
                    for i in data
                ]
                return elems
            except:
                return []
    return []


async def gather_tasks():
    dates = [f'01.07.{i}' for i in range(1992, 2022)]
    tasks = [get_historical_currencies_info(date) for date in dates]
    result = await asyncio.gather(*tasks)
    return result


def process():
    results = asyncio.run(gather_tasks())

    import itertools
    import json

    items = list(itertools.chain.from_iterable(results))

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)

    codes = sorted(list(set(i['code'] for i in data)))
    print(codes)
    currencies = {i: {} for i in codes}

    for k, v in currencies.items():
        for i in data:
            if k == i['code']:
                v['cbr_id'] = i['cbr_id']
                v['name'] = i['name']
                v['nominal'] = i['nominal']

    with open('currencies.json', 'w', encoding='utf-8') as f:
        json.dump(currencies, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    process()