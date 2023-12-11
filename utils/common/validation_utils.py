from datetime import datetime

import holidays
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox


def validate_date(date):
    datetime.strptime(date, '%d/%m/%y')


def validate_start_date_and_today(start_date):
    """
    Validate that the start date is greater or equal to the date today
    :param start_date:
    :return: Bool
    """
    date_today = datetime.now()
    start_date = datetime.strptime(start_date, '%d/%m/%y')
    if start_date.date() >= date_today.date():
        return True
    return False


def validate_date_end(end_date, start_date):
    """
    Validate that the end date is greater than the start_date
    :param start_date:
    :param end_date:
    :return:
    """
    end_date = datetime.strptime(end_date, '%d/%m/%y')
    start_date = datetime.strptime(start_date, '%d/%m/%y')
    if end_date > start_date:
        return True
    return False


def validate_date_is_not_holiday_or_weekend(date):
    """
    Return True if the date is not in the holiday or weekend
    :param date:
    :return:
    """
    ar_holidays = holidays.country_holidays(country="AR")
    date = datetime.strptime(date, '%d/%m/%y')
    if date.weekday() != 5 and date.weekday() != 6:
        if ar_holidays.get(str(date.date())) is None:
            return True
    return False

