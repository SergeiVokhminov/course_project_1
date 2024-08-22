import json
import logging
import os
from typing import Any

import pandas as pd

from src.utils import (exchange_rate, get_info_card, get_json_file, price_share, prints_a_greeting,
                       top_five_transactions)

#  Путь до XLSX-файла
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/views.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("views")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_file(filename: str = "data/operations.xlsx") -> Any:
    """
    Функция для считывания финансовых операций из Excel.
    :param filename: Принимает путь к файлу Excel в качестве аргумента.
    :return: Выводит список словарей с транзакциями.
    """

    try:
        pd_excel = pd.read_excel(filename)
        return pd_excel.to_dict(orient="records")
    except Exception as ex:
        print(f"Неверный формат файла. Ошибка {ex}")


def views_main(data: str, transactions: Any) -> Any:
    """
    Функция объединяет все вспомогательные функции и выводит результат.
    :param data: Принимает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS.
    :param transactions: Принимает список словарей с транзакциями.
    :return: Возвращает JSON-ответ со следующими данными:
            - приветствие в зависимости от текущего времени.
            - информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк).
            - топ-5 транзакций по сумме платежа.
            - курс валют.
            - стоимость акций из S&P500.
    """

    try:
        logger.info("Функция views начала работу.")
        transaction_file = read_file(transactions)
        greeting = prints_a_greeting(data)
        info_card = get_info_card(transaction_file)
        five_transaction = top_five_transactions(transaction_file)
        user_setting = get_json_file()
        currency = exchange_rate(user_setting[0])
        stock = price_share(user_setting[1])
        logger.info("Функция объединяет полученные результаты.")
        result_dict = {
            "greeting": greeting,
            "cards": info_card,
            "top_transaction": five_transaction,
            "currency_rate": currency,
            "stock_price": stock,
        }
        logger.info("Функция views завершила работу и вывела результат.")
        return json.dumps(result_dict, ensure_ascii=False)
    except Exception as ex:
        logger.info(f"Функция views завершила работу с ошибкой {ex}")
        raise Exception(f"При работе функции произошла ошибка {ex}")


if __name__ == "__main__":
    print(views_main("2024-08-16 18:57:35", PATH_TO_FILE))
