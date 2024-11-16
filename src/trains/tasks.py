from celery import shared_task


@shared_task
def trains_list_parsing(user_id: int) -> None:
    pass
