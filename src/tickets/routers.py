from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from common.types import RailwayTicketServices

from tickets.tasks import get_tickets_recent_info

router = Router(name='tickets')


@router.message(Command('tickets'))
async def run_command_handler(message: Message) -> None:
    await message.answer('Получаем данные о билетах из Москвы в Санкт-Петербург на 26.12.2024...')
    task = await get_tickets_recent_info.kiq(
        1,
        'https://www.tutu.ru/poezda/wizard/seats/?departure_st=2000000&arrival_st=2004000&dep_st=2006004&arr_st=2004001&tn=022%D0%90&date=26.12.2024+00%3A25%3A00&search-uid=2135f973-e06d-48ef-9b7e-42284286f987',
        RailwayTicketServices.TUTURU,
    )
    result = await task.wait_result()
    tickets = result.return_value

    await message.answer('Ответ получен!')
    await message.answer(str(len(tickets)))
