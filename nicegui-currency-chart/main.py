from nicegui import ui, app

from utils import get_chart


@ui.page('/')
async def index():
    output = ui.row()
    with output:
        chart = await get_chart()
        ui.chart(chart).classes('lg:w-full')


ui.run(dark=True, title='Курсы валют ЦБ РФ', port=8081)
