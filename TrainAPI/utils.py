from django.conf import settings
from TrainAPI.models import Station, Train
from django.utils.timezone import activate


def GetListStation():
    line_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17]
    station_ids = Station.objects.filter(lineId__in=line_ids).values_list('id', flat=True)
    list_stations = list(station_ids)
    count = len(list_stations)
    return {'count': count, 'data': list_stations}

def GetListMoscow():
    activate(settings.TIME_ZONE)
    trains = Train.objects.values().filter(line=2, id__startswith='775_753')
    result = list(trains)
    return result
