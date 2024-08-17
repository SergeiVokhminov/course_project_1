import json
import os
import re
import pandas as pd
import logging

from typing import List, Dict

#  Путь до XLSX-файла
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/services.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("services")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_file(filename: str = "data/operations.xlsx"):
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


def simple_search(transactions: str | List[Dict], search: str) -> str | List[Dict]:
    """
    Функция обрабатывает список словарей с транзакциями по строке для поиска.
    :param transactions: Принимает список словарей транзакций.
    :param search: Принимает строку для поиска.
    :return: Возвращает JSON-ответ со всеми транзакциями.
    """

    logger.info(f"Функция simple_search начала работу, строка для поиска: {search}")
    transaction_list = []
    logger.info("Функция формирует ответ")
    for transaction in transactions:
        if (
            search == transaction.get("Описание")
            or search == transaction.get("Категория")
        ):
            transaction_list.append(transaction)
    logger.info("Функция simple_search завершила работу и вывела результат.")
    return json.dumps(transaction_list, ensure_ascii=False)


def filter_numbers(transaction: list | str) -> list | str:
    """
    Функция фильтрует список по номерам телефона в описании.
    :param transaction: Принимает список с транзакциями.
    :return: Выводит список с транзакциями отфильтрованный по номерам телефона.
    """
    logger.info("Функция filter_numbers начала работу.")
    new_list_filter = []
    logger.info("Функция фильтрует список по номерам телефона.")
    for item in transaction:
        if "Описание" in item and re.findall(
                r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", item.get("Описание"), flags=re.IGNORECASE
        ):
            new_list_filter.append(item)
    logger.info("Функция filter_numbers завершила работу.")
    return json.dumps(new_list_filter, ensure_ascii=False)


if __name__ == "__main__":
    print(simple_search(read_file(PATH_TO_FILE), "Переводы"))
    print()
    print(filter_numbers(read_file(PATH_TO_FILE)))
