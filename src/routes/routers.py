import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from routes.tasks import get_route_services_info

router = Router(name="routes")


@router.message(Command("run"))
async def run_command_handler(message: Message) -> None:
    await message.answer(
        "Получаем данные о пути из Новосибирска в Усть-кут на 18.12.2024..."
    )
    task = await get_route_services_info.kiq(
        "Новосибирск", "Усть-кут", datetime.date(2024, 12, 18)
    )
    result = await task.wait_result()
    routes = result.return_value

    await message.answer("Ответ получен!")
    await message.answer(str(routes))
