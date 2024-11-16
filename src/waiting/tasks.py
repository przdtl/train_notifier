from celery import shared_task


@shared_task
def waiting_list_parsing(user_id: int) -> None:
    pass
