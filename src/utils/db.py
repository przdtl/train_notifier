import motor.motor_asyncio

from utils.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(host=settings.MONGODB_CONF.DB_HOST,
                                                port=settings.MONGODB_CONF.DB_PORT,
                                                username=settings.MONGODB_CONF.DB_USER,
                                                password=settings.MONGODB_CONF.DB_PASS,
                                                authSource="admin")

db = client.get_database(settings.MONGODB_CONF.DB_NAME)
