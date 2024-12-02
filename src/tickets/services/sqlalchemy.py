from sqlalchemy import select

from common.db import async_session_maker

from tickets.types import Ticket as TicketType
from tickets.models import Ticket as TicketModel


async def get_tickets_by_train(train_id: int) -> list[TicketModel]:
    """
    Возвращает список билетов для заданного ID поезда

    Args:
        train_id (int): ID поезда

    Returns:
        list[Ticket]: Список билетов, соответствующих ID поезда
    """
    async with async_session_maker() as session:
        query = select(TicketModel).where(TicketModel.train_id == train_id)
        result = await session.execute(query)

        return list(result.scalars().all())


async def synchronize_tickets_info(
    train_id: int, tickets: list[TicketType]
) -> list[TicketModel]:
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

        added_tickets: list[TicketModel] = []
        for ticket in tickets:
            new_ticket = TicketModel(
                number=ticket.get("number"),
                carriage_number=ticket.get("carriage_number"),
                vertical_shelf_placement=ticket.get("vertical_shelf_placement"),
                horisontal_shelf_placement=ticket.get("horisontal_shelf_placement"),
                carriage_type=ticket.get("carriage_type"),
                train_id=train_id,
            )
            session.add(new_ticket)
            added_tickets.append(new_ticket)

        await session.commit()

        return added_tickets
