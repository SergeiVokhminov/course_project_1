import json

from config import setup_logger, PATH_TO_FILE
from read_files import read_file
from utils import (prints_a_greeting, get_info_card, top_five_transactions,
                   get_json_file, exchange_rate, price_share)

logger = setup_logger("views", "logs/views.log")


def views_main(data: str, transactions):
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
            "stock_price": stock
        }
        logger.info("Функция views завершила работу и вывела результат.")
        return json.dumps(result_dict, ensure_ascii=False)
    except Exception as ex:
        logger.info(f"Функция views завершила работу с ошибкой {ex}")
        raise Exception(f"При работе функции произошла ошибка {ex}")


if __name__ == "__main__":
    print(views_main("2024-08-16 18:57:35", PATH_TO_FILE))
