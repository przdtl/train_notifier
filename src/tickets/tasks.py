from celery import shared_task


@shared_task
def tickets_list_parsing(user_id: int) -> None:
    pass
