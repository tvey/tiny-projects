import httpx
import xmltodict

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

CURRENCIES = {
    'AUD': {
        'cbr_id': 'R01010',
        'name': 'Австралийский доллар',
        'nominal': '1',
    },
    'AZN': {
        'cbr_id': 'R01020A',
        'name': 'Азербайджанский манат',
        'nominal': '1',
    },
    'GBP': {
        'cbr_id': 'R01035',
        'name': 'Фунт стерлингов Соединенного королевства',
        'nominal': '1',
    },
    'AMD': {
        'cbr_id': 'R01060',
        'name': 'Армянских драмов',
        'nominal': '100',
    },
    'BYN': {
        'cbr_id': 'R01090B',
        'name': 'Белорусский рубль',
        'nominal': '1',
    },
    'BGN': {
        'cbr_id': 'R01100',
        'name': 'Болгарский лев',
        'nominal': '1',
    },
    'BRL': {
        'cbr_id': 'R01115',
        'name': 'Бразильский реал',
        'nominal': '1',
    },
    'HUF': {
        'cbr_id': 'R01135',
        'name': 'Венгерских форинтов',
        'nominal': '100',
    },
    'HKD': {
        'cbr_id': 'R01200',
        'name': 'Гонконгских долларов',
        'nominal': '10',
    },
    'DKK': {
        'cbr_id': 'R01215',
        'name': 'Датская крона',
        'nominal': '1',
    },
    'USD': {
        'cbr_id': 'R01235',
        'name': 'Доллар США',
        'nominal': '1',
    },
    'EUR': {
        'cbr_id': 'R01239',
        'name': 'Евро',
        'nominal': '1',
    },
    'INR': {
        'cbr_id': 'R01270',
        'name': 'Индийских рупий',
        'nominal': '100',
    },
    'KZT': {
        'cbr_id': 'R01335',
        'name': 'Казахстанских тенге',
        'nominal': '100',
    },
    'CAD': {
        'cbr_id': 'R01350',
        'name': 'Канадский доллар',
        'nominal': '1',
    },
    'KGS': {
        'cbr_id': 'R01370',
        'name': 'Киргизских сомов',
        'nominal': '100',
    },
    'CNY': {
        'cbr_id': 'R01375',
        'name': 'Китайский юань',
        'nominal': '1',
    },
    'MDL': {
        'cbr_id': 'R01500',
        'name': 'Молдавских леев',
        'nominal': '10',
    },
    'NOK': {
        'cbr_id': 'R01535',
        'name': 'Норвежских крон',
        'nominal': '10',
    },
    'PLN': {
        'cbr_id': 'R01565',
        'name': 'Польский злотый',
        'nominal': '1',
    },
    'RON': {
        'cbr_id': 'R01585F',
        'name': 'Румынский лей',
        'nominal': '1',
    },
    'XDR': {
        'cbr_id': 'R01589',
        'name': 'СДР (специальные права заимствования)',
        'nominal': '1',
    },
    'SGD': {
        'cbr_id': 'R01625',
        'name': 'Сингапурский доллар',
        'nominal': '1',
    },
    'TJS': {
        'cbr_id': 'R01670',
        'name': 'Таджикских сомони',
        'nominal': '10',
    },
    'TRY': {
        'cbr_id': 'R01700J',
        'name': 'Турецких лир',
        'nominal': '10',
    },
    'TMT': {
        'cbr_id': 'R01710A',
        'name': 'Новый туркменский манат',
        'nominal': '1',
    },
    'UZS': {
        'cbr_id': 'R01717',
        'name': 'Узбекских сумов',
        'nominal': '10000',
    },
    'UAH': {
        'cbr_id': 'R01720',
        'name': 'Украинских гривен',
        'nominal': '10',
    },
    'CZK': {
        'cbr_id': 'R01760',
        'name': 'Чешских крон',
        'nominal': '10',
    },
    'SEK': {
        'cbr_id': 'R01770',
        'name': 'Шведских крон',
        'nominal': '10',
    },
    'CHF': {
        'cbr_id': 'R01775',
        'name': 'Швейцарский франк',
        'nominal': '1',
    },
    'ZAR': {
        'cbr_id': 'R01810',
        'name': 'Южноафриканских рэндов',
        'nominal': '10',
    },
    'KRW': {
        'cbr_id': 'R01815',
        'name': 'Вон Республики Корея',
        'nominal': '1000',
    },
    'JPY': {
        'cbr_id': 'R01820',
        'name': 'Японских иен',
        'nominal': '100',
    },
}


async def get_rates(date: str = ''):
    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params={'date_req': date})

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}
    print(rates)

    return rates | {'$': rates['USD'], '€': rates['EUR']}


async def get_dynamic_rates(cbr_code: str, date_one: str, date_two: str = ''):
    params = {
        'VAL_NM_RQ': cbr_code,
        'date_req1': date_one,
        'date_req2': date_one,
    }
    if date_two:
        params['date_req2'] = date_two

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DYNAMIC, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Record']

    return [{'date': i['@Date'], 'value': i['Value']} for i in data]


async def calculate(direction, currency_code, amount):
    rates = await get_rates()
    currency_rate = float(rates.get(currency_code).replace(',', '.'))
    nominal = int(CURRENCIES[currency_code]['nominal'])
    result = 0

    if direction == 'from_rub':
        result = amount / currency_rate * nominal
    elif direction == 'to_rub':
        result = amount * currency_rate / nominal
    return result
