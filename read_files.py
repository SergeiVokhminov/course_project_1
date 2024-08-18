import json
import pandas as pd

from typing import Any


# Считывает EXCEL-файл и преобразовывает его в DataFrame
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


# Считывает EXCEL-файл и преобразует его в список словарей
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


# Открытие файла с пользовательскими настройками в виде JSON-файла
def read_user_setting(filename: str = "user_settings.json") -> Any:
    """
    Функция обрабатывает файл с пользовательскими настройками.
    :param filename: Принимает файл с пользовательскими настройками.
    :return: Возвращает JSON-файл с пользовательскими настройками.
    """

    with open(filename, encoding="UTF-8") as f:
        load_json = json.load(f)
        return load_json
