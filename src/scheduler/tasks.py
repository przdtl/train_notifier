import asyncio

from aiogram import Bot

from dataclasses import dataclass

from typing import TypedDict, Coroutine, Any

from taskiq import TaskiqDepends

from common.broker import broker
from common.types import RailwayTicketServices

from routes.models import Route
from routes.services.sqlalchemy import get_user_routes

from trains.models import Train
from trains.tasks import get_trains_recent_info
from trains.services.sqlalchemy import get_trains_by_route

from tickets.models import Ticket
from tickets.tasks import get_tickets_recent_info
from tickets.services.sqlalchemy import get_tickets_by_train


@dataclass
class TrainsDiff:
    updated: list[Train] = []
    added: list[Train] = []
    no_changed: list[Train] = []


@dataclass
class TicketsDiff:
    added: list[Ticket] = []
    deleted: list[Ticket] = []


@broker.task
async def get_recent_info(user_id: int, bot: Bot = TaskiqDepends()) -> None:
    user_routes = await get_user_routes(user_id)

    old_route_trains: dict[int, dict[int, Train]] = {}
    trains_coros: list[Coroutine[Any, Any, tuple[Route, list[Train]]]] = []

    for route in user_routes:
        old_trains = await get_trains_by_route(route._id)
        old_route_trains.update({route._id: {train._id: train for train in old_trains}})

        trains_coros.append(
            run_and_get_result_from_recent_trains_info(
                route, route.railway_ticket_service
            )
        )

    route_trains = dict(await asyncio.gather(*trains_coros))

    old_train_tickets: dict[int, dict[int, Ticket]] = {}
    tickets_coros: list[Coroutine[Any, Any, tuple[Train, list[Ticket]]]] = []

    for route, trains in route_trains.items():
        for train in trains:
            old_tickets = await get_tickets_by_train(train._id)
            old_train_tickets.update(
                {train._id: {ticket._id: ticket for ticket in old_tickets}}
            )

            tickets_coros.append(
                run_and_get_result_from_recent_tickets_info(
                    train, route.railway_ticket_service
                )
            )

    train_tickets = dict(await asyncio.gather(*tickets_coros))

    routes_train_diff = get_routes_train_differences(old_route_trains, route_trains)
    trains_tickets_diff = get_train_tickets_differences(
        old_train_tickets, train_tickets
    )

    await answer_info_diff(bot, routes_train_diff, trains_tickets_diff)


async def run_and_get_result_from_recent_trains_info(
    route: Route, ticket_service: RailwayTicketServices
) -> tuple[Route, list[Train]]:
    task = await get_trains_recent_info.kiq(
        route._id,
        route.url,
        ticket_service,
    )
    task_result = await task.wait_result()

    return route, task_result.return_value


async def run_and_get_result_from_recent_tickets_info(
    train: Train, ticket_service: RailwayTicketServices
) -> tuple[Train, list[Ticket]]:
    task = await get_tickets_recent_info.kiq(
        train._id,
        train.url,
        ticket_service,
    )
    task_result = await task.wait_result()

    return train, task_result.return_value


def get_routes_train_differences(
    old_route_trains: dict[int, dict[int, Train]],
    route_trains: dict[Route, list[Train]],
) -> dict[Route, TrainsDiff]:
    routes_train_diff: dict[Route, TrainsDiff] = {}

    for route, trains in route_trains.items():
        added_trains: list[Train] = []
        updated_trains: list[Train] = []
        no_changed: list[Train] = []

        old_trains = old_route_trains.get(route._id) or {}
        for train in trains:
            old_train = old_trains.get(train._id)
            if old_train is None:
                added_trains.append(train)
                continue

            if train.status == old_train.status:
                no_changed.append(train)
                continue

            updated_trains.append(train)

        routes_train_diff.update(
            {
                route: TrainsDiff(
                    updated=updated_trains,
                    added=added_trains,
                    no_changed=no_changed,
                )
            }
        )

    return routes_train_diff


def get_train_tickets_differences(
    old_train_tickets: dict[int, dict[int, Ticket]],
    train_tickets: dict[Train, list[Ticket]],
) -> dict[int, TicketsDiff]:
    train_tickets_diff: dict[int, TicketsDiff] = {}

    for train, tickets in train_tickets.items():
        added_trains: list[Ticket] = []
        deleted_trains: list[Ticket] = []

        old_tickets_set: set[int] = set()

        old_tickets = old_train_tickets.get(train._id) or {}
        for ticket in tickets:
            old_ticket = old_tickets.get(ticket._id)
            if old_ticket is not None:
                old_tickets_set.add(ticket._id)
                continue

            added_trains.append(ticket)

        for ticket_id, ticket in old_tickets.items():
            if ticket_id in old_tickets_set:
                continue

            deleted_trains.append(ticket)

        train_tickets_diff.update(
            {
                train._id: TicketsDiff(
                    added=added_trains,
                    deleted=deleted_trains,
                )
            }
        )

    return train_tickets_diff


async def answer_info_diff(
    bot: Bot,
    /,
    routes_train_diff: dict[Route, TrainsDiff],
    trains_tickets_diff: dict[int, TicketsDiff],
) -> None:
    text = ""

    for route, trains_diff in routes_train_diff.items():
        # header = header_template.format(
        #     _from=route._from,
        #     to=route.to,
        #     date=route.date,
        #     service=route.railway_ticket_service.capitalize,
        # )
        no_changed_trains_list = trains_diff.no_changed
        for train in no_changed_trains_list:
            train_tickets_diff = trains_tickets_diff.get(train._id)
            if train_tickets_diff is None:
                break

            added_tickets_list = train_tickets_diff.added
            deleted_tickets_list = train_tickets_diff.deleted

            added_tickets_count = len(added_tickets_list)
            deleted_tickets_count = len(deleted_tickets_list)

        added_trains_list = trains_diff.added
        added_trains_header = "\nНовые поезда:" if added_trains_list else ""
        added_trains_body = ""
        for train in added_trains_list:
            train_tickets_diff = trains_tickets_diff.get(train._id)
            if train_tickets_diff is None:
                break

            added_tickets_list = train_tickets_diff.added
            added_tickets_count = len(added_tickets_list)

            deleted_tickets_list = train_tickets_diff.deleted
            deleted_tickets_count = len(deleted_tickets_list)
