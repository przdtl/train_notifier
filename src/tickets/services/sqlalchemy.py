from sqlalchemy import select

from common.db import async_session_maker

from tickets.types import Ticket as TicketType
from tickets.models import Ticket as TicketModel


async def synchronize_tickets_info(train_id: int, tickets: list[TicketType]) -> None:
    """
    Синхронизирует список поездов в базе данных с предоставленным списком

    Args:
        train_id (int): ID поезда
        tickets (List[Ticket]): Список билетов, которые нужно синхронизировать
    """
    async with async_session_maker() as session:
        await session.execute(
            TicketModel.__table__.delete().where(TicketModel.train_id == train_id)
        )

        for ticket in tickets:
            session.add(
                TicketModel(
                    number=ticket.get("number"),
                    carriage_number=ticket.get("carriage_number"),
                    vertical_shelf_placement=ticket.get("vertical_shelf_placement"),
                    horisontal_shelf_placement=ticket.get("horisontal_shelf_placement"),
                    carriage_type=ticket.get("carriage_type"),
                    train_id=train_id,
                )
            )

        await session.commit()
