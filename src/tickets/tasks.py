
from common.broker import broker
from common.types import RailwayTicketServices

from tickets.types import Ticket
from tickets.parser_factory import parser_factory
from tickets.services.sqlalchemy import synchronize_tickets_info


@broker.task
async def get_tickets_recent_info(train_id: int, train_url: str, ticket_service: RailwayTicketServices) -> list[Ticket]:
    parser = parser_factory.create_parser(ticket_service)
    tickets = await parser.parse(train_url)

    await synchronize_tickets_info(train_id, tickets)

    return tickets
