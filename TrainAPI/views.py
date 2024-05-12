from datetime import datetime, timedelta
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import concurrent.futures
from django.utils.timezone import activate

from TrainAPI.models import Station, Train, Wagon
from TrainAPI.request import station_request
from TrainAPI.utils import GetListMoscow, GetListStation

def request_station_view(request, station_id):
    api_url = f'https://prodapp.mosmetro.ru/api/stations/v2/{station_id}/wagons/'
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            json_data = response.json()['data']
            return JsonResponse({'status': 'ok', 'tatus_code': response.status_code, 'data': json_data})
        else:
            return JsonResponse({'status': 'ok', 'tatus_code': response.status_code, 'data': 'error'})
    except Exception as e:
        return JsonResponse({'status': 'ok', 'tatus_code': 500, 'data': str(e)})
    
def GenerationListStation(request):
    api_url = 'https://prodapp.mosmetro.ru/api/schema/v1.0/'
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            json_data = response.json()
            all_stations = [station for station in json_data['data']['stations']]
            filtered_data = [{
                "id": station["id"],
                "name_ru": station["name"]["ru"],
                "name_en": station["name"].get("en", ""),
                "lineId": station["lineId"],
                } for station in all_stations]
            
            for station_data in filtered_data:
                station = Station(
                id=station_data["id"],
                lineId=station_data["lineId"],
                name_ru=station_data["name_ru"],
                name_en=station_data["name_en"]
                )
                station.save()
            return JsonResponse({'status': 'ok', 'tatus_code': response.status_code, 'data': 'Данные успешно сохранены в базу данных'})
        else:
            return JsonResponse({'status': 'ok', 'tatus_code': response.status_code, 'data': 'error'})
    except Exception as e:
        return JsonResponse({'status': 'ok', 'tatus_code': 500, 'data': str(e)})
    

def update(request):
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
                
    return JsonResponse({'status': 'ok', 'data': 'ok', 'countOK': countOK, 'countError': countError, 'responses': list_stations})

def update_train(request, station_id):
    response = station_request(station_id)
    lineid = response.get('lineid')
    data = response.get('data')
    for station_id, trains in data.items():
        for train in trains:
            trainDB, created = Train.objects.get_or_create(
                id = train['id'],
                    defaults={
                        'line': lineid,
                        'way': train['way'],
                        'prev_station': train['prevStation'],
                        'next_station': train['nextStation'],
                        'arrival_time': train['arrivalTime'],
                        'train_index': train['trainIndex'],
                        }

            )

            for wagon, status in train['wagons'].items():
                wagonDB, created = Wagon.objects.get_or_create(
                    train = trainDB,
                    number = wagon,
                    defaults={
                        'wagon_type': status
                        }
                )

    return JsonResponse({'status': 'ok', 'data': 'ok'})


def get_moscow_msg(request):
    result = GetListMoscow()
    print(result)
    if result is None:
        return HttpResponse('Поезда не найдены')
    
    strings = ''
    
    for data in result:
        mod_time = data['modification_time']
        datatime_info = mod_time.strftime('%H:%M:%S %d-%m-%Y')
        
        arrival_time_seconds = data['arrival_time']
        arrival_time_delta = timedelta(seconds=arrival_time_seconds)
        
        future_time = mod_time + arrival_time_delta
        io_future_time_str = future_time.strftime('%H:%M:%S')
        future_time_str  = future_time.strftime('%H:%M:%S %d-%m-%Y')
        
        now_time = datetime.now()
        
        future_time_datetime = datetime.strptime(future_time_str, '%H:%M:%S %d-%m-%Y')
        time_difference =  now_time - future_time_datetime
        
        if time_difference > timedelta(hours=1):
            continue
        
        strings += f"Поезд: {data['id']} \n"
        strings += f"{ Station.objects.get(id = data['prev_station_id']).name_ru} -> {Station.objects.get(id = data['next_station_id']).name_ru} \n"
        strings += f"Прибудет примерно {io_future_time_str}  \n"
        strings += '\n'
    
    return HttpResponse(strings)


# def get_moscow_msg(request):
#     result = GetListMoscow()
#     if result is None:
#         return JsonResponse({'data': 'trains not found'})
    
#     return JsonResponse({'data': result})


    