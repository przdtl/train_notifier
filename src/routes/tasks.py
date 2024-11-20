import asyncio
import datetime

from common.broker import broker

from routes.services.playwright import TutuTicketsParser


@broker.task
async def taaask():
    parser = TutuTicketsParser()
    await asyncio.sleep(5)
    url = await parser.parse(
        'Новосибирск',
        'Усть-кут',
        datetime.date(2024, 12, 18)
    )
    print(f'{url=}')
