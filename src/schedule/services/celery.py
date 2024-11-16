from celery.schedules import crontab

from mycelery import app
from schedule.tasks import parsing_schedule


def schedule_periodic_task(user_id: int):
    # Уникальное имя для задачи (например, по user_id)
    task_name = f"periodic_task_{user_id}"

    # Удаляем старую задачу, если такая уже была
    app.control.revoke(task_name, terminate=True)

    # Добавляем новую задачу на выполнение каждую минуту
    app.add_periodic_task(
        crontab(minute='*/1'),
        parsing_schedule.s(user_id),
        name=task_name
    )
