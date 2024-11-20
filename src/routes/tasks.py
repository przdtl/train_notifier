import asyncio
import datetime

from common.celery import app
from common.utils import run_async

from routes.services.playwright import TutuTicketsParser


async def foo():
    parser = TutuTicketsParser()
    await asyncio.sleep(5)
    url = await parser.parse(
        'Новосибирск',
        'Усть-кут',
        datetime.date(2024, 12, 18)
    )
    print(f'{url=}')


@app.task
async def taaask():
    parser = TutuTicketsParser()
    await asyncio.sleep(5)
    url = await parser.parse(
        'Новосибирск',
        'Усть-кут',
        datetime.date(2024, 12, 18)
    )
    print(f'{url=}')
