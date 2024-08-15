#  Основные функции для генерации JSON-ответов
#  Функция для страницы "Главная"
#  Функция для страницы "События"
import json

from config import setup_logger, PATH_TO_FILE
from read_files import read_file
from src.utils import (prints_a_greeting, get_info_card, get_json_file,
                       top_five_transactions, exchange_rate, price_share)

logger = setup_logger("views", "../logs/views.log")


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
        # info_card = get_info_card(transactions_file)
        five_transaction = top_five_transactions(transaction_file)
        user_setting = get_json_file()
        currency = exchange_rate(user_setting[0])
        stock = price_share(user_setting[1])
        logger.info("Функция объединяет полученные результаты.")
        result_dict = {
            "greeting": greeting,
            "top_transaction": five_transaction,
            "currency_rate": currency,
            "stock_price": stock
        }
        result_json = json.dumps(result_dict, ensure_ascii=False)
        logger.info("Функция views завершила работу и вывела результат.")
        return result_json
    except Exception as ex:
        logger.info(f"Функция views завершила работу с ошибкой {ex}")
        raise Exception(f"При работе функции произошла ошибка {ex}")


if __name__ == "__main__":
    print(views_main("2024-08-16 18:57:35", PATH_TO_FILE))
