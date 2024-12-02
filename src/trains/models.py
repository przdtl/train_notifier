import datetime

from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import Base

from trains.types import TrainStatus


class Train(Base):
    """
    Данные о поезде
    """

    __tablename__ = "train"

    _id: Mapped[int] = mapped_column("id", primary_key=True)

    number: Mapped[str] = mapped_column(nullable=False)
    trip_time: Mapped[datetime.timedelta] = mapped_column(nullable=False)
    departure_datetime: Mapped[datetime.datetime] = mapped_column(nullable=False)
    arrival_datetime: Mapped[datetime.datetime] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TrainStatus] = mapped_column(Enum(TrainStatus), nullable=False)
    route_service_id: Mapped[int] = mapped_column(
        ForeignKey("route_service.id", ondelete="CASCADE"), nullable=False
    )

    route_service: Mapped["RouteRailwayService"] = relationship(back_populates="trains")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="train")
    train_status: Mapped["TrainTicketsStatus"] = relationship(back_populates="train")

    __table_args__ = (
        UniqueConstraint("number", "route_id", name="unique_train_for_every_route"),
    )


class RouteTrainsStatus(Base):
    """
    Информация о состоянии последнего парсинга поездов
    """

    __tablename__ = "route_trains_status"

    route_id: Mapped[int] = mapped_column(
        ForeignKey("route_service.id"), primary_key=True
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=lambda: datetime.datetime.now(datetime.timezone.utc).replace(
            tzinfo=None
        ),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc).replace(
            tzinfo=None
        ),
        nullable=False,
    )

    route_service: Mapped["RouteRailwayService"] = relationship(
        back_populates="route_status"
    )
