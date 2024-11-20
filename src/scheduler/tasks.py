from celery import shared_task


@shared_task
def parsing_scheduling_task(user_id: int) -> None:
    pass
