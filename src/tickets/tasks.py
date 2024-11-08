from pydantic import AnyUrl

from mycelery import app

from common.services.selenium import TutuParser


@app.task
def run_task() -> None:
    url = AnyUrl('https://www.tutu.ru/poezda/wizard/seats/?departure_st=2044000&arrival_st=2054290&dep_st=2044001&arr_st=2054290&tn=097%D0%A1&date=18.12.2024+00%3A32%3A00&search-uid=ce4f918d-c45a-4907-b97f-9ec8adfe4213')
    parser = TutuParser()
    carriages = parser.get_tickets_list(url)
    for carriage in carriages:
        for ticket in carriage.tickets:
            print(ticket)
        print(carriage.category, carriage.number, carriage.price)

    parser._close_browser()
