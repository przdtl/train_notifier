import multiprocessing

from pydantic import AnyUrl

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command

from services.selenium import TutuParser

router = Router()


def foo():
    url = AnyUrl('https://www.tutu.ru/poezda/wizard/seats/?departure_st=2044000&arrival_st=2054290&dep_st=2044001&arr_st=2054290&tn=097%D0%A1&date=18.12.2024+00%3A32%3A00&search-uid=ce4f918d-c45a-4907-b97f-9ec8adfe4213')
    parser = TutuParser()
    carriages = parser.get_tickets_list(url)
    for carriage in carriages:
        for ticket in carriage.tickets:
            print(ticket)
        print(carriage.category, carriage.number, carriage.price)

    parser._close_browser()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message(Command('run'))
async def command_run_handler(message: Message) -> None:
    process = multiprocessing.Process(target=foo)
    process.start()
    await message.answer('ok')


@router.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
