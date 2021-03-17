from typing import Final
from multiprocessing import Process

import requests
import time

from task import task_1, task_2, task_3
from task3_flask import app

HOST: Final = "127.0.0.1"
PORT: Final = 5000
TARGET: Final = "/api"


def pretty_print(func):
    def wrapper(*args, **kwargs):
        print("_" * 10 + f"{func.__name__}:" + "_" * 10)
        func(*args, **kwargs)

    return wrapper


@pretty_print
def show_task_1(s) -> None:
    print(f"given string '{s}'\nreturn {task_1(s)}")


@pretty_print
def show_task_2(debug: bool = False) -> None:
    task_2(debug)


@pretty_print
def show_task_3(data) -> None:
    print(f"given data '{data}'\nreturn {task_3(data)}")


@pretty_print
def show_task_3_flask(host: str, port: int) -> None:
    process = Process(target=flask_process, args=(host, port))
    process.start()
    # даем время на запуск
    time.sleep(2)
    print(f'given data "{data}"\nas json in {url}')
    r = requests.get(f'{url}', json=data)
    print(f"and return {r.json()}")
    process.terminate()


def flask_process(host: str, port: int):
    app.run(host=host, port=port)


if __name__ == '__main__':
    s = '11010'
    data = {
        'lesson': [1594663200, 1594666800],
        'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
        'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
    }
    url = f"http://{HOST}:{PORT}/{TARGET}"
    show_task_1(s)
    show_task_2(True)
    show_task_3(data)
    show_task_3_flask(HOST, PORT)
