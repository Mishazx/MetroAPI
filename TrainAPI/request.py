import datetime
import requests

from TrainAPI.models import Station, Train, Wagon


def station_request(station_id):
    api_url = f'https://prodapp.mosmetro.ru/api/stations/v2/{station_id}/wagons/'
    # station = Station.objects.get(id=station_id)
    # lineid = station.lineId
    # try:
    station = Station.objects.get(id=station_id)
    lineid = station.lineId

    # except Station.DoesNotExist:
    #     print(station_id)
    #     return {'status': 'error', 'essage': 'Station not found', 'status_code': 404}
    
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            json_data = response.json()['data'] 
            for station_id, trains in json_data.items():
                for train in trains:
                    trainDB, created = Train.objects.get_or_create(
                        id = train['id'],
                                          defaults={
                        'line': lineid,
                        'way': train['way'],
                        'prev_station': Station.objects.get(id=train['prevStation']),
                        'next_station': Station.objects.get(id=train['nextStation']),
                        'arrival_time': train['arrivalTime'],
                        'train_index': train['trainIndex'],
                        'modification_time': datetime.datetime.now()
                        }
                    )
                    
                    if not created:
                        Train.objects.filter(id=train['id']).update(
                        line=lineid,
                        way=train['way'],
                        prev_station=Station.objects.get(id=train['prevStation']),
                        next_station=Station.objects.get(id=train['nextStation']),
                        arrival_time=train['arrivalTime'],
                        train_index=train['trainIndex'],
                        modification_time=datetime.datetime.now()
                    )

                    for wagon, status in train['wagons'].items():
                        wagonDB, created = Wagon.objects.get_or_create(
                            train = trainDB,
                            number = wagon,
                            defaults={
                            'wagon_type': status
                            }
                        )
                        
                        if not created:
                            Wagon.objects.filter(train=trainDB, number=wagon).update(
                                wagon_type=status
                            )
                            
            print(station_id, lineid, response.text)
            return {'status': 'ok', 'status_code': response.status_code, 'lineid': lineid, 'data': json_data}
        else:
            print({'error': response.status_code})
            return {'status': 'error', 'status_code': response.status_code, 'data': response.text}
    except Exception as e:
        print({'error': response.status_code, 'exc' : str(e)})
        return {'status': 'error', 'status_code': response.status_code, 'data': str(e)}
    