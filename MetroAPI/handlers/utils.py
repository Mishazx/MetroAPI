import json

from MetroAPI.handlers.request import request


def load_data_stations():
    with open('stations.json', 'r') as file:
        data = json.load(file)
    return data


def getInfoInterval():
    dict_stations = load_data_stations()

    list_of_dicts = []
    for i in dict_stations:
        data = request(i['id'])
        result = data['data']
        list_of_dicts.append(result)
        
    return list_of_dicts