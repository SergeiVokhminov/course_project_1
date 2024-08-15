#  Функции сервиса "Выгодные категории повышенного кэшбэка"
#  (принимает год, месяц для расчета и транзакции в формате списка словарей)

#  Функции сервиса "Инвесткопилка" (принимает месяц для расчета,
#  транзакции в формате списка словарей и лимит округления)
#  отдает корректный JSON-ответ

#  Функции сервиса "Простой поиск" (принимает строку - запрос для поиска и транзакции в формате списка словарей)
#  отдает корректный JSON-ответ ГОТОВО

#  Функция сервиса "Поиск по телефонным номерам" (принимает транзакции в формате списка словарей)
#  отдает корректный JSON-ответ

#  Функция сервиса "Поиск переводов физическим лицам" (принимает транзакции в формате списка словарей)
#  отдает корректный JSON-ответ

import json

from typing import List, Dict
from src.utils import read_file
from config import PATH_TO_FILE, setup_logger

logger = setup_logger("services", "../logs/services.log")


def simple_search(transactions: List[dict], search: str) -> List[Dict]:
    """
    Функция обрабатывает список словарей с транзакциями по строке для поиска.
    :param transactions: Принимает список словарей транзакций.
    :param search: Принимает строку для поиска.
    :return: Возвращает JSON-ответ со всеми транзакциями.
    """
    logger.info(f"Функция начала работу, строка для поиска: {search}")
    transactions_read = read_file(transactions)
    transaction_list = []
    for transaction in transactions_read:
        if (
            search == transaction.get("Описание")
            or search == transaction.get("Категория")
        ):
            transaction_list.append(transaction)
    logger.info("Функция завершила работу")
    return json.dumps(transaction_list, ensure_ascii=False)


if __name__ == "__main__":
    print(simple_search(PATH_TO_FILE, "Переводы"))
