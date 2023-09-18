import datetime
from collections import OrderedDict

import httpx
import xmltodict

# from httpx import AsyncClient
# from httpx_caching import CachingClient

URL_DAILY = 'http://www.cbr.ru/scripts/XML_daily.asp'
URL_DYNAMIC = 'http://www.cbr.ru/scripts/XML_dynamic.asp'


def format_date(date: datetime.date | str) -> str:
    """Format a date string or object for use in a URL parameter."""
    if isinstance(date, datetime.date):
        return date.strftime('%d/%m/%Y')
    else:
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y').strftime(
                '%d/%m/%Y'
            )
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
    date_one: str | datetime.date,
    date_two: str | datetime.date = '',
) -> list:
    """Get rates for one currency for one date or a specified date span."""
    params = {
        'VAL_NM_RQ': cbr_id,
        'date_req1': format_date(date_one),
        'date_req2': format_date(date_one),
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


def line_chart(
    series: list[dict],
    date_range: list[datetime.date],
    colors: list[str],
):
    chart = {
        'chart': {
            # 'backgroundColor': chart_bg_color,
            'spacingTop': 25,
            # 'height': chart_height,
            # 'width': chart_width,
        },
        'title': {
            'text': '',
        },
        'series': series,
        'colors': colors,
        'xAxis': {
            'categories': date_range,
            'labels': {
                'style': {
                    'color': '#fff',
                }
            },
        },
        'yAxis': {
            # 'max': get_yaxis_max(chart_unit, series),
            # 'tickInterval': get_tick_interval(chart_unit, series),
            'title': {
                # 'text': chart_unit_format[chart_unit]['xaxis_text'],
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
        # 'legend': legend_style,
        'tooltip': {
            # 'shared': True,
            # 'valueSuffix': chart_unit_format[chart_unit]['value_suffix'],
            'headerFormat': '<span style=\'font-size:12px\'><b>{point.key}</b></span><br>',
        },
        'plotOptions': {
            'series': {
                'label': {
                    'connectorAllowed': False,
                },
                'lineWidth': 4,
            }
        },
        'responsive': {
            'rules': [
                {
                    'condition': {
                        'maxWidth': 500,
                    },
                    'chartOptions': {
                        'legend': {
                            'layout': 'horizontal',
                            'align': 'center',
                            'verticalAlign': 'bottom',
                        }
                    },
                }
            ]
        },
        'credits': {
            'enabled': False,
        },
    }

    if series:
        for i in series:
            i['marker'] = {'enabled': False}

    return chart


async def get_chart():
    return {}
