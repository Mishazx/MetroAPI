from celery import shared_task
from MetroAPI.celery import app
from TrainAPI.request import station_request
from TrainAPI.utils import GetListStation


@app.task(name='tasks.main_task')
def main_task():
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