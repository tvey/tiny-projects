import httpx
import xmltodict


async def get_rates():
    async with httpx.AsyncClient() as client:
        r = httpx.get('https://www.cbr.ru/scripts/XML_daily.asp')

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = {i['CharCode']: i['Value'] for i in data}

    return {'$': rates['USD'], '€': rates['EUR']}
