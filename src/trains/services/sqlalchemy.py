from sqlalchemy import select

from trains.types import Train as TrainType
from trains.models import Train as TrainModel

from common.db import async_session_maker


async def synchronize_trains_info(route_id: int, trains: list[TrainType]) -> None:
    """
    Синхронизирует список поездов в базе данных с предоставленным списком

    Args:
        route_id (int): ID маршрута
        trains (List[Train]): Список поездов, которые нужно синхронизировать
    """
    async with async_session_maker() as session:
        db_trains_query = select(TrainModel).where(TrainModel.route_id == route_id)
        result = await session.execute(db_trains_query)
        db_trains = {train.number: train for train in result.scalars()}

        trains_dict = {train.get('number'): train for train in trains}

        for number, train_data in trains_dict.items():
            if number in db_trains:
                db_train = db_trains[number]
                db_train.status
                if db_train.status != train_data.get('status'):
                    db_train.status = train_data.get('status')
            else:
                new_train = TrainModel(
                    number=train_data.get('number'),
                    trip_time=train_data.get('trip_time'),
                    departure_datetime=train_data.get('departure_datetime'),
                    arrival_datetime=train_data.get('arrival_datetime'),
                    url=train_data.get('url'),
                    route_id=route_id,
                    status=train_data.get('status'),
                )
                session.add(new_train)

        for number, db_train in db_trains.items():
            if number not in trains_dict:
                await session.delete(db_train)

        await session.commit()
