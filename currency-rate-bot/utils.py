import httpx
import xmltodict


async def get_rates():
    async with httpx.AsyncClient() as client:
        r = httpx.get('https://www.cbr.ru/scripts/XML_daily.asp')

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    return rates | {'$': rates['USD'], '€': rates['EUR']}


CURRENCIES = [
    {
        'code': 'AUD',
        'nominal': '1',
        'name': 'австралийский доллар',
    },
    {
        'code': 'AZN',
        'nominal': '1',
        'name': 'азербайджанский манат',
    },
    {
        'code': 'GBP',
        'nominal': '1',
        'name': 'фунт стерлингов',
    },
    {
        'code': 'AMD',
        'nominal': '100',
        'name': 'армянских драмов',
    },
    {
        'code': 'BYN',
        'nominal': '1',
        'name': 'белорусский рубль',
    },
    {
        'code': 'BGN',
        'nominal': '1',
        'name': 'болгарский лев',
    },
    {
        'code': 'BRL',
        'nominal': '1',
        'name': 'бразильский реал',
    },
    {
        'code': 'HUF',
        'nominal': '100',
        'name': 'венгерских форинтов',
    },
    {
        'code': 'HKD',
        'nominal': '1',
        'name': 'гонконгский доллар',
    },
    {
        'code': 'DKK',
        'nominal': '1',
        'name': 'датская крона',
    },
    {
        'code': 'USD',
        'nominal': '1',
        'name': 'доллар США',
    },
    {
        'code': 'EUR',
        'nominal': '1',
        'name': 'евро',
    },
    {
        'code': 'INR',
        'nominal': '10',
        'name': 'индийских рупий',
    },
    {
        'code': 'KZT',
        'nominal': '100',
        'name': 'казахстанских тенге',
    },
    {
        'code': 'CAD',
        'nominal': '1',
        'name': 'канадский доллар',
    },
    {
        'code': 'KGS',
        'nominal': '100',
        'name': 'киргизских сомов',
    },
    {
        'code': 'CNY',
        'nominal': '1',
        'name': 'китайский юань',
    },
    {
        'code': 'MDL',
        'nominal': '10',
        'name': 'молдавских леев',
    },
    {
        'code': 'NOK',
        'nominal': '10',
        'name': 'норвежских крон',
    },
    {
        'code': 'PLN',
        'nominal': '1',
        'name': 'польский злотый',
    },
    {
        'code': 'RON',
        'nominal': '1',
        'name': 'румынский лей',
    },
    {
        'code': 'SGD',
        'nominal': '1',
        'name': 'сингапурский доллар',
    },
    {
        'code': 'TJS',
        'nominal': '10',
        'name': 'таджикских сомони',
    },
    {
        'code': 'TRY',
        'nominal': '10',
        'name': 'турецких лир',
    },
    {
        'code': 'TMT',
        'nominal': '1',
        'name': 'новый туркменский манат',
    },
    {
        'code': 'UZS',
        'nominal': '10000',
        'name': 'узбекских сумов',
    },
    {
        'code': 'UAH',
        'nominal': '10',
        'name': 'украинских гривен',
    },
    {
        'code': 'CZK',
        'nominal': '10',
        'name': 'чешских крон',
    },
    {
        'code': 'SEK',
        'nominal': '10',
        'name': 'шведских крон',
    },
    {
        'code': 'CHF',
        'nominal': '1',
        'name': 'швейцарский франк',
    },
    {
        'code': 'ZAR',
        'nominal': '10',
        'name': 'южноафриканских рэндов',
    },
    {
        'code': 'KRW',
        'nominal': '1000',
        'name': 'вон Республики Корея',
    },
    {
        'code': 'JPY',
        'nominal': '100',
        'name': 'японских иен',
    },
]
