import datetime

from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import Base

from tickets.types import VerticalShelfPlacement, HorisontalShelfPlacement, CarriageType


class Ticket(Base):
    """
    Данные о билете
    """

    __tablename__ = "ticket"

    _id: Mapped[int] = mapped_column("id", primary_key=True)

    number: Mapped[int] = mapped_column(nullable=False)
    carriage_number: Mapped[int] = mapped_column(nullable=False)
    vertical_shelf_placement: Mapped[VerticalShelfPlacement] = mapped_column(
        Enum(VerticalShelfPlacement), nullable=False
    )
    horisontal_shelf_placement: Mapped[HorisontalShelfPlacement] = mapped_column(
        Enum(HorisontalShelfPlacement), nullable=False
    )
    carriage_type: Mapped[CarriageType] = mapped_column(
        Enum(CarriageType), nullable=False
    )
    train_id: Mapped[int] = mapped_column(
        ForeignKey("train.id", ondelete="CASCADE"), nullable=False
    )

    train: Mapped["Train"] = relationship(back_populates="tickets")

    __table_args__ = (
        UniqueConstraint(
            "train_id",
            "carriage_number",
            "number",
            name="Unique ticket number for every carriage for every train",
        ),
    )


class TrainTicketsStatus(Base):
    """
    Информация о состоянии последнего парсинга билетов
    """

    __tablename__ = "train_tickets_status"

    train_id: Mapped[int] = mapped_column(ForeignKey("train.id"), primary_key=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now(datetime.timezone.utc).replace(
            tzinfo=None
        ),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc).replace(
            tzinfo=None
        ),
        nullable=False,
    )

    train: Mapped["Train"] = relationship(back_populates="train_status")
