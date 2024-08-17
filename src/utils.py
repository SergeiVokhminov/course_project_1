import json
import os
import logging
import requests
import pandas as pd

from datetime import datetime
from collections import defaultdict
from typing import Any, List, Dict
from dotenv import load_dotenv

#  Путь до XLSX-файла
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/utils.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

load_dotenv()
apilayer_token = os.getenv("API_KEY")
alphavantage_token = os.getenv("API_KEY_STOCK")


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


def prints_a_greeting(date_str: str):
    """
    Функция выводит приветствие в зависимости от текущего времени.
    :param date_str: Принимает строку с датой и времени в формате YYYY-MM-DD HH:MM:SS
    :return: Возвращает JSON-ответ
    """
    logger.info(f"Функция prints_a_greeting начало работу.")
    greeting_dict = {
        "1": ("Доброе утро.", "05:00:01", "12:00:00"),
        "2": ("Добрый день.", "12:00:01", "18:00:00"),
        "3": ("Добрый вечер.", "18:00:01", "23:59:59"),
        "4": ("Доброй ночи.", "00:00:00", "05:00:00"),
    }
    try:
        data_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        time_greeting = data_obj.time()
        logger.info("Функция анализирует и обрабатывает полученные данные.")
        for item in greeting_dict:
            start = greeting_dict[item][1]
            finish = greeting_dict[item][2]
            start_time = datetime.strptime(start, "%H:%M:%S").time()
            finish_time = datetime.strptime(finish, "%H:%M:%S").time()
            if start_time <= time_greeting <= finish_time:
                logger.info("Функция prints_a_greeting завершила работу и вывела результат.")
                return greeting_dict.get(item)[0]
    except Exception:
        logger.info(f"Функция prints_a_greeting завершила работу с ошибкой.")
        raise ValueError(f"Введены неверные данные!")


def get_info_card(transactions: List[Dict]) -> Any:
    """
    Функция обрабатывает список словарей с транзакциями и выводит результат.
    :param transactions: Список словарей с транзакциями.
    :return: Выводит информацию по каждой карте (последние 4 цифры, общую сумму расходов,
    кэшбэк (1 рубль на каждые 100 рублей)).
    """

    logger.info("Функция get_info_card начала работу.")
    unique_card_nums = list(set([transaction.get("Номер карты") for transaction in transactions]))
    expenditure_by_card = defaultdict(int)
    logger.info("Функция обрабатывает данные.")
    for card_num in unique_card_nums:
        for transaction in transactions:
            if transaction["Номер карты"] == card_num:
                expenditure_by_card[card_num] += transaction.get("Сумма операции")
    result_transaction_list = []
    logger.info("Функция формирует итоговый результат.")
    for item in expenditure_by_card:
        result_transaction_list.append(
            {
                "last_digits": item[1:],
                "total_spent": round(expenditure_by_card[item], 2),
                "cashback": round(expenditure_by_card[item] / 100, 2),
            }
        )
    logger.info("Функция get_info_card завершила работу.")
    return result_transaction_list


def top_five_transactions(transactions: List[Dict]) -> Any:
    """
    Функция выводит топ-5 транзакций по сумме платежа.
    :param transactions: Список словарей с транзакциями.
    :return: Выводит топ-5 транзакций по сумме платежа.
    """
    logger.info("Функция top_five_transactions начала работу.")
    total_expenses = [total.get("Сумма платежа") for total in transactions if total.get("Сумма платежа") >= 0]

    top_five = sorted([expenses for expenses in total_expenses if expenses is not None], reverse=True)[:5]

    last_top = [transaction for transaction in transactions if transaction.get("Сумма платежа") in top_five]

    if last_top:
        result = []
        for transaction in last_top[:5]:
            result.append(
                {
                    "date": transaction.get("Дата платежа"),
                    "amount": transaction.get("Сумма платежа"),
                    "category": transaction.get("Категория"),
                    "description": transaction.get("Описание"),
                }
            )
        logger.info("Функция top_five_transactions завершила работу и вывела результат.")
        return result
    else:
        logger.info("Функция top_five_transactions завершила работу и вывела пустой список.")
        return []


def get_json_file(path: str = "user_settings.json") -> Any:
    """
    Функция обрабатывает JSON-файл пользовательских настроек.
    :param path: Принимает JSON-файл.
    :return: Возвращает списков валют и акций.
    """
    logger.info("Функция get_json_file начала работу.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info("Функция get_json_file завершила работу.")
            return data.get("user_currencies"), data.get("user_stocks")
    except Exception:
        logger.error("Возникла ошибка при обработке файла пользовательских настроек!")
        raise Exception("Возникла ошибка при обработке файла!")


def exchange_rate(currency: List) -> Any:
    """
    Функция обращается к API и выводит курс валют.
    :param currency: Принимает наименование валюты.
    :return: Выводит курс валют.
    """
    logger.info("Функция exchange_rate начала работу.")
    try:
        result_currency_list = []
        for exchange in currency:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={"RUB"}&from={exchange}&amount={1}"
            headers = {"apikey": apilayer_token}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            result_currency_list.append({"currency_rates": exchange, "rate": round(float(result["result"]), 2)})
        logger.info("Функция exchange_rate завершила работу и вывела результат.")
        return result_currency_list
    except Exception as ex:
        logger.info(f"Функция exchange_rate завершила работу с ошибкой {ex}!")
        raise Exception("Неизвестная валюта")


def price_share(stocks: List) -> Any:
    """
    Функция обращается к API и выводит курс акций.
    :param stocks: Принимает наименование акций.
    :return: Выводит стоимость акций
    """
    logger.info("Функция price_share начала работу.")
    try:
        result_stocks_list = []
        logger.info("Функция получает данные по ценам акций.")
        for stock in stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={alphavantage_token}"
            response = requests.get(url)
            result = response.json()
            result_stocks_list.append({"stock": stock, "price": round(float(result["Global Quote"]["05. price"]), 2)})
            logger.info("Функция завершила свою работу.")
        return result_stocks_list
    except Exception as ex:
        logger.error(f"Функция price_share завершила свою работу с ошибкой {ex}!")
        raise Exception("При работе функции произошла ошибка!")


if __name__ == "__main__":
    print(prints_a_greeting("2024-08-14 18:56:44"))
    print(get_info_card(read_file(PATH_TO_FILE)))
    print(top_five_transactions(read_file(PATH_TO_FILE)))
    print(exchange_rate(["USD", "EUR"]))
    print(price_share(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]))
