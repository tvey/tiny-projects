import datetime
import json
from collections import OrderedDict

import httpx
import xmltodict

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'


def get_intervals():
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    if today.month != 1:
        month_ago = today.replace(month=today.month - 1)
    else:
        month_ago = today.replace(year=today.year - 1, month=12)
    try:
        year_ago = today.replace(year=today.year - 1)
    except ValueError:
        year_ago = today.replace(year=today.year - 1, day=today.day - 1)
    two_years_ago = year_ago.replace(year=year_ago.year - 1)
    five_years_ago = today.replace(year=year_ago.year - 4)

    intervals = {
        '5 дней': [week_ago.date(), today.date()],
        'месяц': [month_ago.date(), today.date()],
        'год': [year_ago.date(), today.date()],
        '2 года': [two_years_ago.date(), today.date()],
        '5 лет': [five_years_ago.date(), today.date()],
    }
    return intervals


def get_currencies(display=False):
    with open('currencies.json', encoding='utf-8') as f:
        currencies = json.load(f)

    if display:
        return {k: v['name_singular'] for k, v in currencies.items()}
    return currencies


def format_date(date: datetime.date | str) -> str:
    """Format a date string or object for use in a URL parameter."""
    url_format = '%d/%m/%Y'
    if isinstance(date, datetime.date):
        return date.strftime(url_format)
    else:
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').strftime(url_format)
        except (TypeError, ValueError):
            raise Exception('Bad date value')


async def get_rates(date: datetime.date | None = None) -> list[dict]:
    """Get rates of available currencies for the current or historical date."""
    params = {'date_req': format_date(date)} if date else {}

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DAILY, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Valute']
    rates = [
        {
            'char_code': i['CharCode'],
            'name': i['Name'],
            'nominal': i['Nominal'],
            'value': float(i['Value'].replace(',', '.')),
        }
        for i in data
    ]
    return rates


async def get_dynamic_rates(
    cbr_id: str,
    date_one: str,
    date_two: str = '',
) -> list:
    """Get rates for one currency for one date or a specified date span."""
    params = {
        'VAL_NM_RQ': cbr_id,
        'date_req1': date_one,
        'date_req2': date_one,
    }

    if date_two:
        params['date_req2'] = date_two

    async with httpx.AsyncClient() as client:
        r = await client.get(URL_DYNAMIC, params=params)

    data = xmltodict.parse(r.content)['ValCurs']['Record']

    if isinstance(data, OrderedDict):
        data = [data]

    return [
        {
            'date': i['@Date'],
            'nominal': i['Nominal'],
            'value': float(i['Value'].replace(',', '.')),
        }
        for i in data
    ]


def line_chart(
    title: str,
    series: list[dict],
    date_range: list[datetime.date],
):
    chart = {
        'chart': {
            'backgroundColor': '#121212',
            'height': 600,
        },
        'title': {
            'text': title,
            'style': {
                'color': '#fff',
            },
        },
        'series': series,
        'xAxis': {
            'categories': date_range,
            'labels': {
                'style': {
                    'color': '#fff',
                }
            },
        },
        'yAxis': {
            'title': {
                'text': '',
                'style': {
                    'color': '#fff',
                },
            },
            'labels': {
                'style': {
                    'color': '#fff',
                }
            },
        },
        'legend': {
            'enabled': False,
        },
        'tooltip': {
            'valueSuffix': ' ₽',
            'headerFormat': '<span style=\'font-size:12px\'><b>{point.key}</b></span><br>',
        },
        'plotOptions': {
            'series': {
                'label': {
                    'connectorAllowed': False,
                },
                'lineWidth': 2,
            }
        },
        'credits': {
            'enabled': False,
        },
    }

    if series:
        for i in series:
            i['marker'] = {'enabled': False}

    return chart


def get_date_range(
    start: datetime.date,
    end: datetime.date,
) -> list[datetime.date]:
    """Return start, end dates and all the dates in between."""
    delta_days = (end - start).days + 1
    return [start + datetime.timedelta(days=i) for i in range(delta_days)]


async def get_chart(cbr_id: str, start: datetime.date, end: datetime.date):
    currency = get_currencies()[cbr_id]
    title = f"{currency['nominal']} {currency['name']}"
    rates = await get_dynamic_rates(cbr_id, format_date(start), format_date(end))
    date_range = [i['date'] for i in rates]
    series = [
        {
            'name': f"{currency['nominal']} {currency['char_code']}",
            'data': [i['value'] for i in rates],
            'color': '#5898d4',
        }
    ]
    chart = line_chart(title, series, date_range)
    return chart
