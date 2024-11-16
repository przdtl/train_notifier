from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from mongodb import trains_collection
from trains.documents import Train


class TrainService:
    def __init__(self, trains_collection: AsyncIOMotorCollection[Train] = trains_collection) -> None:
        self.collection = trains_collection

    async def create_train(self, train_instance: Train) -> ObjectId:
        result = await self.collection.insert_one(train_instance)

        return result.inserted_id

    async def get_train(self, **kwargs) -> Train | None:
        return await self.collection.find_one(kwargs)
