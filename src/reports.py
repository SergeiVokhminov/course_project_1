import os
import logging
import pandas as pd

from datetime import datetime, timedelta
from typing import Optional, Any, Callable

#  Путь до XLSX-файла
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/reports.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_exel_df(filename: str = "data/operations.xlsx") -> pd.DataFrame:
    """
    Функция читает и обрабатывает EXCEL-файл.
    :param filename: Принимает путь до EXCEL-файл.
    :return: Возвращает EXCEL-файл в формате DataFrame.
    """

    try:
        df = pd.read_excel(filename)
        return df
    except Exception as ex:
        raise Exception(f"Ошибка при обработке файла {ex}!")


def report_to_file(func: Callable) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info("Декоратор report_to_file начал работу")
        result = func(*args, **kwargs)
        with open("../report_file.txt", "w", encoding="UTF-8") as f:
            f.write(str(result))
        return result

    logger.info("Декоратор report_to_file завершил работу")
    return wrapper


@report_to_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    :param transactions: Принимаем DataFrame транзакций.
    :param category: Принимает категорию.
    :param date: Принимает дату.
    :return: Возвращает DataFrame трат за последние три месяца по переданной категории и дате.
    """

    logger.info(f"Функция spending_by_category начала работу. Категория: {category}, Дата: {date}")
    if date is None:
        parsed_date = datetime.now()
    else:
        parsed_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    transactions = transactions[transactions["Сумма операции"] < 0]
    transactions = transactions[transactions["Категория"] == category]

    end_data = parsed_date - timedelta(days=90)

    transactions = transactions[pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= parsed_date]

    transactions = transactions[pd.to_datetime(transactions["Дата операции"], dayfirst=True) > end_data]
    logger.info("Функция spending_by_category завершила работу и вывела результат")
    return pd.DataFrame(transactions)


if __name__ == "__main__":
    print(spending_by_category(read_exel_df(PATH_TO_FILE), "Фастфуд", "29.11.2020 14:40:00"))
