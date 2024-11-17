from typing import TypedDict

import motor.motor_asyncio

from common.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(host=settings.MONGODB_CONF.DB_HOST,
                                                port=settings.MONGODB_CONF.DB_PORT,
                                                username=settings.MONGODB_CONF.DB_USER,
                                                password=settings.MONGODB_CONF.DB_PASS,
                                                authSource="admin")

db = client.get_database(settings.MONGODB_CONF.DB_NAME)


trains = db.get_collection(settings.MONGODB_CONF.Collections.TRAINS.value)
tickets = db.get_collection(settings.MONGODB_CONF.Collections.TICKETS.value)
waitings = db.get_collection(settings.MONGODB_CONF.Collections.WAITINGS.value)
