import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from routes.tasks import get_route_info

from common.types import RailwayTicketServices

from trains.tasks import get_trains_recent_info

router = Router(name='scheduler')


@router.message(Command('sch'))
async def run_command_handler(message: Message) -> None:
    await message.answer('Получаем данные о поездах из Новосибирска в Иркутск на 30.12.2024...')
    task = await get_route_info.kiq(
        'Новосибирск',
        'Иркутск',
        datetime.date(2024, 12, 30)
    )
    result = await task.wait_result()
    route = result.return_value[0]

    url = route.get('url')

    await message.answer(url)

    task = await get_trains_recent_info.kiq(
        1,
        url,
        RailwayTicketServices.TUTURU,
    )
    result = await task.wait_result()
    trains = result.return_value

    await message.answer('Ответ получен!')
    await message.answer(str(trains))
