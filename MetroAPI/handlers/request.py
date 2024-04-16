import requests


def request(station_id):
    api_url = f'https://prodapp.mosmetro.ru/api/stations/v2/{station_id}/wagons/'
    try:
        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            json_data = response.json()['data'] 
            return {'status': 'ok', 'status_code': response.status_code, 'data': json_data}
        else:
            return {'status': 'ok', 'status_code': response.status_code, 'data': 'error'}
    except Exception as e:
        return {'status': 'ok', 'status_code': response.status_code, 'data': str(e)}