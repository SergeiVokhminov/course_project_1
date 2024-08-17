#  Основные настройки
import os
import logging

#  Корневая директория проекта
ROOT_DIR = os.path.dirname(__file__)
# print(ROOT_DIR)

#  Путь до XLSX-файла
PATH_TO_FILE = os.path.join(ROOT_DIR, "..", "data", "operations.xlsx")


#  Настройки для логгера
def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настойка логгера, включает метку времени,
    название модуля, уровень серьезности и сообщение,
    описывающее событие или ошибку, которая произошла."""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file, "w", encoding="UTF-8")
    file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
