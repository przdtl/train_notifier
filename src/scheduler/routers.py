import asyncio
import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from routes.tasks import get_route_services_info

from common.types import RailwayTicketServices

from trains.tasks import get_trains_recent_info

from tickets.types import Ticket
from tickets.tasks import get_tickets_recent_info

router = Router(name="scheduler")


@router.message(Command("sch"))
async def run_command_handler(message: Message) -> None:
    await message.answer(
        "Получаем данные о поездах из Новосибирска в Иркутск на 31.12.2024..."
    )
    task = await get_route_services_info.kiq(
        "Новосибирск", "Иркутск", datetime.date(2024, 12, 31)
    )
    result = await task.wait_result()
    services_route = result.return_value
    tuturu_route = services_route[0]

    await message.answer(str(tuturu_route))

    url = tuturu_route.url

    task = await get_trains_recent_info.kiq(
        1,
        url,
        RailwayTicketServices.TUTURU,
    )
    result = await task.wait_result()
    trains = result.return_value

    await message.answer(str(trains))

    coros = [
        get_tickets_info(train.get("url"), index)
        for index, train in enumerate(trains, 1)
        if train.get("url") is not None
    ]

    result = await asyncio.gather(*coros)

    for train_tickets in result:
        for ticket in train_tickets:
            message.answer(
                f"tickets count for car №{ticket.get('carriage_number')} = {len(train_tickets)}"
            )

    await message.answer("Ответ получен!")


async def get_tickets_info(train_url: str, index: int) -> list[Ticket]:
    task = await get_tickets_recent_info.kiq(
        index,
        train_url,
        RailwayTicketServices.TUTURU,
    )

    result = await task.wait_result()
    tickets = result.return_value

    return tickets
