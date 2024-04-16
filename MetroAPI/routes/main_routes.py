from flask import redirect, render_template

from MetroAPI import app
from MetroAPI.handlers.metro import get_id_moscow, get_moscow, update, get_count_trains
# from MetroAPI.handlers.db import update as up 


@app.route('/')
def index():
    # return redirect('/get_moscow')
    return render_template('index.html')


@app.route('/get_moscow')
def get_msk():
    data = str(get_moscow())
    return data


@app.route('/update')
def updater():
    try:
        data = update()
        return {'status': 'ok', 'msg': data}, 200
    except Exception as e:
        return {'status': 'error', 'msg': str(e)}, 500


@app.route('/get_id_moscow')
def get_id_msk():
    id = get_id_moscow()
    return {'ids': str(id)}


# Next Patch
# @app.route('/all_count')
# def all_count():
#     count = get_count_trains()

#     return {'count': str(count)}
