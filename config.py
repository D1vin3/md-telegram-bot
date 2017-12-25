# -*- coding: utf-8 -*-
from enum import Enum
import emoji


token = '487689975:AAE0qA8M52YLi4KXBfaANQbbLtvqRVFL0LU'
url = 'https://api.telegram.org/bot{0}/'.format(token)

db_file = "database.vdb"
session_file = "session.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_CHOOSE_CRYPTO = "1"
    S_ENTER_SUM = "2"
    S_CHOOSE_CURRENCY_SITE = "3"
    S_ENTER_CITY = "4"
    S_CHOOSE_MARGINALITY = "5"
