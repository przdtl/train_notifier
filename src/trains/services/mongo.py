from bson import ObjectId

from typing import Any

from common.db import trains


async def create_train(train_instance: dict) -> ObjectId:
    result = await trains.insert_one(train_instance)

    return result.inserted_id


async def get_train(**kwargs) -> Any:
    return await trains.find_one(kwargs)
