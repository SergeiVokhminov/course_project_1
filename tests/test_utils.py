from typing import Any
from unittest.mock import patch

import pytest

from src.utils import exchange_rate, get_info_card, get_json_file, prints_a_greeting, read_file, top_five_transactions


# Тестируем функцию чтения EXCEL-файла
@patch("pandas.read_excel")
def test_excel_ok(mock_read_excel: Any) -> Any:
    mock_read_excel.return_value.to_dict.return_value = [
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        }
    ]
    assert read_file("all_file") == [
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "",
            "Категория": "Красота",
            "MCC": 5977.0,
            "Описание": "OOO Balid",
            "Бонусы (включая кэшбэк)": 6,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 316.0,
        }
    ]


@patch("pandas.read_excel")
def test_excel_error(mock_read_excel: Any) -> Any:
    mock_read_excel.return_value.to_dict.return_value = []


# Тестируем функция, которая выводит приветствие в зависимости от введенной даты
@pytest.fixture
def greeting_fnc() -> str:
    return "2024-08-16 14:11:55"


def test_prints_a_greeting(greeting_fnc: str) -> Any:
    assert prints_a_greeting(greeting_fnc) == "Добрый день."


@pytest.mark.parametrize(
    "date, expected", [("2022-08-16 11:30:00", "Доброе утро."), ("2024-08-17 02:15:00", "Доброй ночи.")]
)
def test_print_a_greetings(date: str, expected: str) -> Any:
    assert prints_a_greeting(date) == expected


def test_greetings_error() -> Any:
    with pytest.raises(ValueError) as ex:
        prints_a_greeting("12asfs")
        assert str(ex.value) == "Введены неверные данные!"


# Тестируем функцию вывода информации по картам
@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {
                    "Дата операции": "18.03.2023 15:44:00",
                    "Дата платежа": "19.03.2023",
                    "Номер карты": "*4567",
                    "Статус": "OK",
                    "Сумма операции": -150.0,
                    "Валюта операции": "EUR",
                    "Сумма платежа": -150.0,
                    "Валюта платежа": "EUR",
                    "Кэшбэк": "",
                    "Категория": "Фастфуд",
                    "MCC": 4814.0,
                    "Описание": "МТС",
                    "Бонусы (включая кэшбэк)": 3,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 150.0,
                },
                {
                    "Дата операции": "11.06.2023 11:23:56",
                    "Дата платежа": "12.06.2023",
                    "Номер карты": "*4567",
                    "Статус": "OK",
                    "Сумма операции": -197.7,
                    "Валюта операции": "EUR",
                    "Сумма платежа": -197.7,
                    "Валюта платежа": "EUR",
                    "Кэшбэк": "nan",
                    "Категория": "Супермаркеты",
                    "MCC": 5411.0,
                    "Описание": "Магнит",
                    "Бонусы (включая кэшбэк)": 3,
                    "Округление на инвесткопилку": 0,
                    "Сумма операции с округлением": 197.7,
                },
            ],
            [{"last_digits": "4567", "total_spent": -347.7, "cashback": -3.48}],
        )
    ],
)
def test_card_info(transactions: list, expected: list[dict]) -> Any:
    assert get_info_card(transactions) == expected


transacrion = read_file("../data/operations.xlsx")


# Тестируем функцию вывода топ-5 транзакций
@pytest.fixture
def top_five_fnc() -> Any:
    return [
        {
            "amount": 174000.0,
            "category": "Пополнения",
            "date": "30.12.2021",
            "description": "Пополнение через Газпромбанк",
        },
        {"amount": 150000.0, "category": "Пополнения", "date": "14.09.2021", "description": "Перевод с карты"},
        {"amount": 150000.0, "category": "Пополнения", "date": "01.08.2020", "description": "Перевод с карты"},
        {
            "amount": 190044.51,
            "category": "Переводы",
            "date": "21.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": 177506.03,
            "category": "Переводы",
            "date": "23.10.2018",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]


def test_top_five_transactions(top_five_fnc: Any) -> None:
    assert top_five_transactions(transacrion) == []


users_settings = {"user_currencies": "EUR"}


@patch("json.load")
def test_json(mock_json: Any) -> None:
    mock_json.return_value = {"user_currencies": ["EUR"], "user_stocks": ["TSLA"]}
    assert get_json_file() == (["EUR"], ["TSLA"])


def test_json_error() -> None:
    with pytest.raises(ValueError) as ex:
        get_json_file("2352sds")
        assert str(ex.value) == "Возникла ошибка при обработке файла!"


# Тестируем функцию работы с курсом валют через API
@patch("requests.get")
def test_currency_rates(mock_test: Any) -> None:
    mock_test.return_value.json.return_value = {"result": 100.20}
    assert exchange_rate(["USD"]) == [{"currency_rates": "USD", "rate": 100.20}]
