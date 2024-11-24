
from common.broker import broker
from common.types import RailwayTicketServices

from trains.types import Train
from trains.parser_factory import parser_factory
from trains.services.sqlalchemy import synchronize_trains_info


@broker.task
async def get_trains_recent_info(route_id: int, route_url: str, ticket_service: RailwayTicketServices) -> list[Train]:
    parser = parser_factory.create_parser(ticket_service)
    trains = await parser.parse(route_url)

    await synchronize_trains_info(route_id, trains)

    return trains
