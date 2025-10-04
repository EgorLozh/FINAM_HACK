from celery import Celery

from app_parsing.settings import settings

celery_app = Celery(
    "parser",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app_parsing.tasks"],
)


celery_app.conf.update(
    task_track_started=True,
)


celery_app.conf.beat_schedule = {
    "run-start-parse-tasks-every-1-hour": {
        "task": "app_parsing.tasks.start_parse_tasks",
        "schedule": 60 * 60,
    },
}
