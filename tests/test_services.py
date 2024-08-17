from typing import Any, Dict, List

import pytest
import json

from src.services import simple_search


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
