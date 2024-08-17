import json
import re


from typing import List, Dict
from read_files import read_file
from config import PATH_TO_FILE, setup_logger

logger = setup_logger("services", "../logs/services.log")


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
