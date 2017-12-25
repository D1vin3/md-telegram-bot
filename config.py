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
    S_TYPE_OWN_CRYPTO = "2"
    S_ENTER_SUM = "3"
    S_CHOOSE_CURRENCY_SITE = "4"
    S_TYPE_OWN_CURRENCY_SITE = "5"
    S_ENTER_CITY = "6"
    S_CHOOSE_MARGINALITY = "7"
