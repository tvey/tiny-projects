from nicegui import ui, app

from utils import (
    get_chart,
    get_currencies,
    get_intervals,
)


@ui.page('/')
async def index():
    intervals = get_intervals()
    storage = app.storage.user
    storage['interval'] = '5 дней'
    storage['currency'] = 'R01235'

    async def update_chart():
        start, end = intervals[storage['interval']]
        chart = await get_chart(storage['currency'], start, end)
        output.clear()
        with output:
            ui.chart(chart).classes('w-full')

    async def handle_interval_button_click(interval):
        storage['interval'] = interval
        show_buttons.refresh()
        await update_chart()

    def get_button(text, color='standard'):
        if text == storage.get('interval'):
            color = 'primary'
        return ui.button(
            text,
            color=color,
            on_click=lambda: handle_interval_button_click(text),
        ).classes('px-3 xl:px-4').props('unelevated')

    @ui.refreshable
    def show_buttons():
        with ui.row():
            for i in intervals.keys():
                get_button(i)

    async def handle_currency_select(currency):
        storage['currency'] = currency
        await update_chart()

    show_buttons()

    output = ui.row().classes('f-full xl:w-1/2')
    with output:
        start, end = intervals[storage['interval']]
        chart = await get_chart(storage['currency'], start, end)
        ui.chart(chart).classes('w-full')

    ui.select(
        options=get_currencies(display=True),
        value='R01235',
        on_change=lambda e: handle_currency_select(e.value),
    ).classes('w-60')


ui.run(dark=True, title='Курсы валют ЦБ РФ', port=8081)
