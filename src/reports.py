import pandas as pd

from datetime import datetime, timedelta
from typing import Optional
from config import PATH_TO_FILE, setup_logger
from read_files import read_exel_df

logger = setup_logger("reports", "logs/reports.log")


def report_to_file_default(func):
    def wrapper(*args, **kwargs):
        logger.info("Декоратор начал работу")
        result = func(*args, **kwargs)
        with open("../report_file.txt", "w", encoding="UTF-8") as f:
            f.write(str(result))
        return result

    logger.info("Декоратор завершил работу")
    return wrapper


@report_to_file_default
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

    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= parsed_date
    ]

    transactions = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) > end_data
    ]
    logger.info("Функция spending_by_category завершила работу и вывела результат")
    return pd.DataFrame(transactions)


if __name__ == "__main__":
    print(spending_by_category(read_exel_df(PATH_TO_FILE), "Фастфуд", "29.11.2020 14:40:00"))
