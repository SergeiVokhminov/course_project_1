import datetime

from src.reports import read_exel_df, spending_by_category
from src.services import simple_search
from src.utils import read_file
from src.views import PATH_TO_FILE, views_main

date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
transactions_list = PATH_TO_FILE


if __name__ == "__main__":
    print(views_main(date, transactions_list))
    print()
    print(spending_by_category(read_exel_df(PATH_TO_FILE), "Переводы", "18.02.2022 14:30:00"))
    print()
    print(simple_search(read_file(PATH_TO_FILE), "Фастфуд"))
    print()
