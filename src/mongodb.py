import motor.motor_asyncio

from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_CONF.DB_URL)
db = client.get_database(settings.MONGODB_CONF.DB_NAME)
trains_collection = db.get_collection(settings.MONGODB_CONF.TRAINS_COLLECTION_NAME)
