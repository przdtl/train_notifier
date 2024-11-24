from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from common.types import RailwayTicketServices

from trains.tasks import get_trains_recent_info

router = Router(name='trains')


@router.message(Command('trains'))
async def run_command_handler(message: Message) -> None:
    await message.answer('Получаем данные о поездах из Новосибирска в Иркутск на 30.12.2024...')
    task = await get_trains_recent_info.kiq(
        1,
        'https://www.tutu.ru/poezda/rasp_d.php?nnst1=2044000&nnst2=2054000&date=30.12.2024',
        RailwayTicketServices.TUTURU,
    )
    result = await task.wait_result()
    trains = result.return_value

    await message.answer('Ответ получен!')
    await message.answer(str(trains))
