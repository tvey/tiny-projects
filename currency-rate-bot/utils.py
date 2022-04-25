import httpx
import xmltodict


async def get_rates():
    async with httpx.AsyncClient() as client:
        r = httpx.get('https://www.cbr.ru/scripts/XML_daily.asp')

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    return rates | {'$': rates['USD'], '€': rates['EUR']}


CURRENCIES = {
    "AUD": {
        "nominal": "1",
        "name": "австралийский доллар",
    },
    "AZN": {
        "nominal": "1",
        "name": "азербайджанский манат",
    },
    "GBP": {
        "nominal": "1",
        "name": "фунт стерлингов",
    },
    "AMD": {
        "nominal": "100",
        "name": "армянских драмов",
    },
    "BYN": {
        "nominal": "1",
        "name": "белорусский рубль",
    },
    "BGN": {
        "nominal": "1",
        "name": "болгарский лев",
    },
    "BRL": {
        "nominal": "1",
        "name": "бразильский реал",
    },
    "HUF": {
        "nominal": "100",
        "name": "венгерских форинтов",
    },
    "HKD": {
        "nominal": "1",
        "name": "гонконгский доллар",
    },
    "DKK": {
        "nominal": "1",
        "name": "датская крона",
    },
    "USD": {
        "nominal": "1",
        "name": "доллар США",
    },
    "EUR": {
        "nominal": "1",
        "name": "евро",
    },
    "INR": {
        "nominal": "10",
        "name": "индийских рупий",
    },
    "KZT": {
        "nominal": "100",
        "name": "казахстанских тенге",
    },
    "CAD": {
        "nominal": "1",
        "name": "канадский доллар",
    },
    "KGS": {
        "nominal": "100",
        "name": "киргизских сомов",
    },
    "CNY": {
        "nominal": "1",
        "name": "китайский юань",
    },
    "MDL": {
        "nominal": "10",
        "name": "молдавских леев",
    },
    "NOK": {
        "nominal": "10",
        "name": "норвежских крон",
    },
    "PLN": {
        "nominal": "1",
        "name": "польский злотый",
    },
    "RON": {
        "nominal": "1",
        "name": "румынский лей",
    },
    "SGD": {
        "nominal": "1",
        "name": "сингапурский доллар",
    },
    "TJS": {
        "nominal": "10",
        "name": "таджикских сомони",
    },
    "TRY": {
        "nominal": "10",
        "name": "турецких лир",
    },
    "TMT": {
        "nominal": "1",
        "name": "новый туркменский манат",
    },
    "UZS": {
        "nominal": "10000",
        "name": "узбекских сумов",
    },
    "UAH": {
        "nominal": "10",
        "name": "украинских гривен",
    },
    "CZK": {
        "nominal": "10",
        "name": "чешских крон",
    },
    "SEK": {
        "nominal": "10",
        "name": "шведских крон",
    },
    "CHF": {
        "nominal": "1",
        "name": "швейцарский франк",
    },
    "ZAR": {
        "nominal": "10",
        "name": "южноафриканских рэндов",
    },
    "KRW": {
        "nominal": "1000",
        "name": "вон Республики Корея",
    },
    "JPY": {
        "nominal": "100",
        "name": "японских иен",
    },
}
