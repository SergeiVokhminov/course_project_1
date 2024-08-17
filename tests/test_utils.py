from typing import Any, Dict, List

import pytest

from unittest.mock import patch
from src.utils import (prints_a_greeting, get_info_card, top_five_transactions,
                       get_json_file, exchange_rate, price_share)


# Тестируем функция, которая выводит приветствие в зависимости от введенной даты
@pytest.fixture
def greeting_fnc():
    return "2024-08-16 14:11:55"


def test_prints_a_greeting(greeting_fnc):
    assert prints_a_greeting(greeting_fnc) == "Добрый день."


@pytest.mark.parametrize(
    "date, expected", [("2022-08-16 11:30:00", "Доброе утро."), ("2024-08-17 02:15:00", "Доброй ночи.")]
)
def test_print_a_greetings(date, expected):
    assert prints_a_greeting(date) == expected


def test_greetings_with_wrong_date():
    with pytest.raises(ValueError) as ex:
        prints_a_greeting("12asfs")
        assert str(ex.value) == "Введены неверные данные!"


# Тестируем функцию вывода топ-5 транзакций
@pytest.fixture
def top_five_fnc():
    return [
        {"date": "30.11.2022",
         "amount": 1500,
         "category": "Пополнение"},
        {"date": "15.10.2022",
         "amount": 1000,
         "category": "Пополнение"},
        {"date": "10.10.2022",
         "amount": 7500,
         "category": "Пополнение"},
        {"date": "16.06.2022",
         "amount": 2500,
         "category": "Пополнение"},
        {"date": "01.08.2022",
         "amount": 3500,
         "category": "Пополнение"}
    ]


def test_top_five_transactions(top_five_fnc):
    assert top_five_transactions(transactions) == top_five_fnc
