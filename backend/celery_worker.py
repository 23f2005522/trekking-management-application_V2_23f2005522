from celery import Celery, Task
from celery.schedules import crontab
from config.config import Config
from main import app


celery_app = Celery(
    "tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["tasks"],
)


# Every task runs inside Flask app context
class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = FlaskTask

celery_app.conf.timezone = "Asia/Kolkata"


celery_app.conf.beat_schedule = {
    "daily-reminder": {
        "task": "tasks.send_daily_trek_reminder",
        # "schedule": 30.0,
        "schedule": crontab(hour=8, minute=0), # daily at 8:00 AM
    },
    "monthly-report": {
        "task": "tasks.send_monthly_admin_report",
        # "schedule": 60.0,
        "schedule": crontab(hour=9, minute=0, day_of_month=1), # monthly at 9:00 AM on the first day of the month
    },
}