# from pydantic import PositiveInt

# from bson import ObjectId
# from motor.motor_asyncio import AsyncIOMotorCollection

# from db import trains_collection
# from documents import Station


# class TrainService:
#     def __init__(self, trains_collection: AsyncIOMotorCollection[Station] = trains_collection) -> None:
#         self.collection = trains_collection

#     async def create_train_station(self, title: str, nnst: PositiveInt, city: str) -> ObjectId:
#         result = await self.collection.insert_one(Station(
#             title=title,
#             nnst=nnst,
#             city=city,
#         ))
#         return result.inserted_id

#     async def get_train_station(self, **kwargs) -> Station | None:
#         return await self.collection.find_one(Station(**kwargs))

#     async def update_train_station_nnst(self, _id: ObjectId, nnst: PositiveInt) -> None:
#         await self.collection.update_one({'_id': _id}, {'$set': {'nnst': nnst}})
