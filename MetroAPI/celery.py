import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MetroAPI.settings')


app = Celery('MetroAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
from celery.beat import Scheduler

app.conf.tasks = ['main_task']

app.conf.beat_schedule = {
    'run-task-every-minute': {
        'task': 'tasks.main_task',
        'schedule': crontab(minute='*/1'), 
    },
}