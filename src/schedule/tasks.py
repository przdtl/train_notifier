from mycelery import app

from trains.tasks import trains_list_parsing
from tickets.tasks import tickets_list_parsing
from waiting.tasks import waiting_list_parsing


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(5.0, parsing_schedule.s(123), name='run task every 5 minutes')


@app.task()
def parsing_schedule(user_id: int) -> None:
    print(user_id)
