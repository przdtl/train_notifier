import datetime

from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.db import Base
from common.types import RailwayTicketServices


class Route(Base):
    """
    Данные о маршруте следования
    """

    __tablename__ = "route"

    _id: Mapped[int] = mapped_column("id", primary_key=True)

    _from: Mapped[str] = mapped_column("from", nullable=False)
    to: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)

    route_users: Mapped[list["ChatRoute"]] = relationship(back_populates="route")
    route_services: Mapped[list["RouteRailwayService"]] = relationship(
        back_populates="route"
    )

    __table_args__ = (UniqueConstraint("from", "to", "date", name="unique_route"),)


class RouteRailwayService(Base):
    """
    Информация о маршруте на определённом сервисе
    """

    __tablename__ = "route_service"

    _id: Mapped[int] = mapped_column("id", primary_key=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), nullable=False
    )

    url: Mapped[str] = mapped_column(nullable=False)
    railway_ticket_service: Mapped[RailwayTicketServices] = mapped_column(
        Enum(RailwayTicketServices), nullable=False
    )

    trains: Mapped[list["Train"]] = relationship(back_populates="route_service")
    route: Mapped["Route"] = relationship(back_populates="route_services")
    route_status: Mapped["RouteTrainsStatus"] = relationship(
        back_populates="route_service"
    )

    __table_args__ = (
        UniqueConstraint(
            "route_id", "railway_ticket_service", name="unique_route_for_every_service"
        ),
    )


class ChatRoute(Base):
    """
    Информация о маршрутах для чата
    """

    __tablename__ = "user_routes"

    chat_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), primary_key=True
    )

    route: Mapped["Route"] = relationship(back_populates="route_users")
