from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings


dp = Dispatcher()
bot = Bot(token=settings.TELEGRAM_CONF.TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML)
)
