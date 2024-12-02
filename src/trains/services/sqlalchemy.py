from sqlalchemy import select

from trains.types import Train as TrainType
from trains.models import Train as TrainModel

from common.db import async_session_maker


async def get_trains_by_route(route_id: int) -> list[TrainModel]:
    """
    Возвращает список поездов для заданного ID маршрута

    Args:
        route_id (int): ID маршрута

    Returns:
        list[Train]: Список поездов, соответствующих ID маршрута
    """
    async with async_session_maker() as session:
        query = select(TrainModel).where(TrainModel.route_id == route_id)
        result = await session.execute(query)

        return list(result.scalars().all())


async def synchronize_trains_info(
    route_id: int, trains: list[TrainType]
) -> list[TrainModel]:
    """
    Синхронизирует список поездов в базе данных с предоставленным списком

    Args:
        route_id (int): ID маршрута
        trains (List[Train]): Список поездов, которые нужно синхронизировать
    """
    async with async_session_maker() as session:
        delete_query = select(TrainModel).where(TrainModel.route_id == route_id)
        result = await session.execute(delete_query)
        db_trains = result.scalars().all()

        for db_train in db_trains:
            await session.delete(db_train)

        added_trains = []
        for train_data in trains:
            new_train = TrainModel(
                number=train_data.get("number"),
                trip_time=train_data.get("trip_time"),
                departure_datetime=train_data.get("departure_datetime"),
                arrival_datetime=train_data.get("arrival_datetime"),
                url=train_data.get("url"),
                route_id=route_id,
                status=train_data.get("status"),
            )
            session.add(new_train)
            added_trains.append(new_train)

        await session.commit()

        return added_trains
