import motor.motor_asyncio

from pymongo.mongo_client import MongoClient

from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(host=settings.MONGODB_CONF.DB_HOST,
                                                port=settings.MONGODB_CONF.DB_PORT,
                                                username=settings.MONGODB_CONF.DB_USER,
                                                password=settings.MONGODB_CONF.DB_PASS,
                                                authSource="admin")

db = client.get_database(settings.MONGODB_CONF.DB_NAME)
trains_collection = db.get_collection(settings.MONGODB_CONF.TRAINS_COLLECTION_NAME)
