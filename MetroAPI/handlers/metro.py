import sqlite3
import requests
import json
from datetime import datetime, timedelta

from MetroAPI.handlers.utils import getInfoInterval


def get_train_data(id):
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trains WHERE id=?", (id,))
    train_data = cursor.fetchone()
    conn.commit()
    conn.close()
    if train_data:
        return train_data
    else:
        return None


def get_id_moscow():
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trains WHERE id LIKE '775_753%'")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    first_values = [arr[0] for arr in rows]
    return first_values


def get_count_trains():
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM trains WHERE modificationTime >= datetime('now') AND modificationTime < datetime('now', '+30 minutes')")
    cursor.execute("SELECT * FROM trains WHERE modificationTime < datetime('now', '2 minutes')")
    # cursor.execute("SELECT COUNT(*) FROM trains WHERE modificationTime <= datetime('now', '2 minutes')")
    # cursor.execute("SELECT * FROM trains WHERE modificationTime < datetime('now', '+20 minutes')")

    # data = cursor.fetchone()[0]
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    data = json.dumps(len(data))
    # first_values = [arr[0] for arr in rows]
    return data


def update():
    data = getInfoInterval()
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS trains 
                    (id TEXT PRIMARY KEY, way TEXT, prevStation INTEGER, nextStation INTEGER, arrivalTime INTEGER, trainIndex INTEGER, wagon1 TEXT, wagon2 TEXT, wagon3 TEXT, wagon4 TEXT, wagon5 TEXT, wagon6 TEXT, wagon7 TEXT, wagon8 TEXT, modificationTime DATETIME)''')

    for dictionary in data:
        for key in dictionary:
            for item in dictionary[key]:
                train_id = item['id']
                way = item['way']
                prev_station = item['prevStation']
                next_station = item['nextStation']
                arrival_time = item['arrivalTime']
                train_index = item['trainIndex']
                wagons = item['wagons']
                wagon1 = wagons.get('1', '')
                wagon2 = wagons.get('2', '')
                wagon3 = wagons.get('3', '')
                wagon4 = wagons.get('4', '')
                wagon5 = wagons.get('5', '')
                wagon6 = wagons.get('6', '')
                wagon7 = wagons.get('7', '')
                wagon8 = wagons.get('8', '')
                modification_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                cursor.execute("INSERT OR REPLACE INTO trains VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (train_id, way, prev_station, next_station, arrival_time, train_index, wagon1, wagon2, wagon3, wagon4, wagon5, wagon6, wagon7, wagon8, modification_time))

    conn.commit()
    conn.close()
    return data


def generationListStation():
    api_url = 'https://prodapp.mosmetro.ru/api/schema/v1.0/'
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            json_data = response.json()
            id_line = 2
            file_name = 'stations.json'
            filtered_stations = [station for station in json_data['data']['stations'] if station.get('lineId') == id_line]
            filtered_data = [{"id": station["id"], "name_ru": station["name"]["ru"]
                                        ,"name_en": station["name"]["en"]} for station in filtered_stations]
            with open(file_name, 'w') as file:
                json.dump(filtered_data, file, indent=4)
            print(f"Данные успешно сохранены в файл '{file_name}'")
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            print(response.json())
    except Exception as e:
        print("Произошла ошибка:", e)


def getNameStation(id):
    with open('stations.json', 'r') as file:
        data = json.load(file)
    name_ru = None
    for station in data:
        if station["id"] == id:
            name_ru = station["name_ru"]
            break
    return name_ru
       
            
def getMessage(id, all):
    data = get_train_data(id)
    if data == None:
        return {'status': 'error', 'data':'Поезд не найден'}
    way = data[1]
    napr = ''
    if way == "ГП1":
        napr = 'север'
    if way == 'ГП2':
        napr = 'юг'
    prevSt = data[2]
    nextSt = data[3]
    
    prevNameSt = getNameStation(prevSt)
    nextNameSt = getNameStation(nextSt)
    
    modification_time_str = data[14]
    modification_time = datetime.strptime(modification_time_str, '%Y-%m-%d %H:%M:%S')
    datatime_info = modification_time.strftime('%H:%M:%S %d-%m-%Y')

    arrival_time_seconds = data[4]
    arrival_time_delta = timedelta(seconds=arrival_time_seconds)

    future_time = modification_time + arrival_time_delta
    future_time_str  = future_time.strftime('%H:%M:%S %d-%m-%Y')

    now_time = datetime.now()

    future_time_datetime = datetime.strptime(future_time_str, '%H:%M:%S %d-%m-%Y')
    time_difference =  now_time - future_time_datetime

    if time_difference > timedelta(hours=1) and all != True:
        return {'status': 'error', 'time': time_difference,'data':'Поезд не найден'}

    return {'status': 'ok', 'data': 
            f'Поезд {id}\nЕдет от {prevNameSt} → {nextNameSt} (на {napr})\nПрибудет на "{nextNameSt}" примерно в {future_time}\nИнформация на: {datatime_info}'}
    
    
def get_moscow(all = False):
    update()
    data = ''
    trains = get_id_moscow()
    for train in trains:
        train_data = getMessage(train, all)
        if train_data['status'] == 'ok':
            data += f"{train_data['data']}\n\n"
    
    if data == '':
        data = "Поездов 'Москва 2024' нет на зеленой ветке"
    return data

def start_service():
    generationListStation()
    