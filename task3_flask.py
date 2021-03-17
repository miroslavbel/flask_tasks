from enum import Enum

from flask import Flask, render_template, request, jsonify

from task3 import task_3

app = Flask('task_3')


class Pages(Enum):
    ROOT = '/'
    INDEX = '/index'
    API = '/api'


@app.route(f'{Pages.ROOT.value}')
@app.route(f'{Pages.INDEX.value}')
@app.route(f'{Pages.INDEX.value}.html')
def index():
    return render_template('index.html', arg=Pages.API.value)


@app.route(f'{Pages.API.value}', methods=["GET", "POST"])
def api():
    """
    Не валидирует полученные данные.

    :return: json с единственным ключом {@code 'time'} или строку если запрос
    не содержит json
    """
    if request.is_json:
        json = request.get_json()
        res = task_3(json)
        return jsonify(time=res)
    else:
        return "This request hasn't json!"


if __name__ == '__main__':
    app.run()
