from celery import shared_task
from MetroAPI import settings
from MetroAPI.celery import app
from TrainAPI.request import station_request
from TrainAPI.utils import GetListStation


@app.task(name='tasks.main_task')
def main_task():
    if not settings.CELERY_MAIN_TASK_ENABLED:
        return
    countOK = 0
    countError = 0
    data = GetListStation()
    list_stations = data.get('data')

    for station in list_stations:
        response = station_request(station)
        if response['status_code'] == 200:
            countOK += 1    
        else:
            countError += 1