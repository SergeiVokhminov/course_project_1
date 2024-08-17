from typing import Any, Dict, List

import pytest
import json

from src.services import simple_search, filter_numbers


def test_simple_search():
    search = "Магазины"
    transactions = [
        {"Описание": "Покупка продуктов", "Категория": "Супермаркеты"},
        {"Описание": "Оплата счета", "Категория": "Утилиты"},
        {"Описание": "Покупка одежды", "Категория": "Магазины"},
    ]
    expected_result = json.dumps(
        [{"Описание": "Покупка одежды", "Категория": "Магазины"}],
        ensure_ascii=False,
    )

    assert simple_search(transactions, search) == expected_result


def test_phone_number():
    transactions = [
        {"Категория": "Мобильная связь", "Описание": "Тинькофф Мобайл +7 995 555-55-55"},
        {"Описание": "Оплата счета", "Категория": "Утилиты"},
        {"Категория": "Мобильная связь", "Описание": "Я МТС +7 921 11-22-33"},
    ]
    expected_result = json.dumps(
        [
            {"Категория": "Мобильная связь", "Описание": "Тинькофф Мобайл +7 995 555-55-55"},
            {"Категория": "Мобильная связь", "Описание": "Я МТС +7 921 11-22-33"}
        ],
        ensure_ascii=False,
    )
    assert filter_numbers(transactions) == expected_result
