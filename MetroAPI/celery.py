import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MetroAPI.settings')


app = Celery('MetroAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
from celery.beat import Scheduler

app.conf.update({
    'CELERY_MAIN_TASK_ENABLED': settings.CELERY_MAIN_TASK_ENABLED
})

app.conf.tasks = ['main_task']

app.conf.beat_schedule = {
    'run-task-every-minute': {
        'task': 'tasks.main_task',
        'schedule': crontab(minute='*/1'), 
    },
}