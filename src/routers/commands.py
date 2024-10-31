import datetime
import multiprocessing

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command

from services.selenium import TutuParser

router = Router()


def foo():
    parser = TutuParser()
    parser.get_trains_list_by_nnst(2044000, 2054290, datetime.date(2024, 12, 18))


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
