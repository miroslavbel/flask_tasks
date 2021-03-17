from typing import Final
from collections import Counter

import requests
from lxml import etree

from task3 import task_3

ANIMAL_BY_ALPHABETICAL_ORDER: Final = r"https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


def task_1(s: str) -> int:
    """
    Возвращает индекс первого символа {@code 0} в данной строке {@code s}. Если
    символ в строке отсутствует, то вернет {@code -1}.

    :param s: строка.
    :return: индекс первого символа {@code 0} или {@code -1}.
    """
    return s.find('0')


def _task_2(debug: bool = False) -> Counter[str]:
    """
    Обращается к Википедии и возвращает количество животных на каждую букву
    русского алфавита. Запросы посылаются синхронно, так что работать может
    долго.

    :raise HTTPError: if an HTTP error occurred.
    :return: {@code Counter}, где ключ - русская заглавная буква, а значение -
    количество животных на каждую букву
    """
    counter = Counter()
    parser = etree.XMLParser(recover=True)
    response = requests.get(ANIMAL_BY_ALPHABETICAL_ORDER)
    while True:
        if debug:
            print(f"work with url '{requests.utils.unquote(response.url)}'")
        response.raise_for_status()
        root = etree.fromstring(response.text, parser=parser)
        # обрабатываем названия животных
        letter_groups = root.xpath(r".//div[contains(@class, 'mw-category')]"
                                   r"//div[contains(@class, 'mw-category-group')]")
        for letter_group in letter_groups:
            letter = letter_group.xpath(r".//h3")[0].text.upper()
            if ord(letter) < ord('А') or ord(letter) > ord('Я'):
                # выходим если начались английские буквы
                return counter
            animal_name_elems = letter_group.xpath(r".//ul//li")
            counter.update({letter: counter[letter] + len(animal_name_elems)})
        # ищем ссылку на следующую страницу
        next_page_elems = root.xpath(r"//*[text() = 'Следующая страница']")
        if len(next_page_elems) == 0:
            break
        else:
            url = r"https://ru.wikipedia.org" + next_page_elems[0].get('href')
            response = requests.get(url)
    return counter


def task_2(debug: bool = False) -> None:
    """
    Обращается к Википедии и печатает количество животных на каждую букву
    русского алфавита. Запросы посылаются синхронно, так что работать может
    долго.

    :raise HTTPError: if an HTTP error occurred.
    """
    counter = _task_2(debug)
    if debug:
        print("----- RESULT -----")
    for letter in sorted(list(counter.keys())):
        print(f"{letter}: {counter[letter]}")
