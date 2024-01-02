from datetime import datetime, timedelta


def get_day_of_the_week(date: str) -> str:
    """
    Returns the day of the week
    :param date:
    :return: str
    """
    date_converted = datetime.strptime(date, "%d/%m/%y")
    date_of_week = date_converted.weekday()

    match date_of_week:
        case 0:
            return "LUNES"
        case 1:
            return "MARTES"
        case 2:
            return "MIERCOLES"
        case 3:
            return "JUEVES"
        case 4:
            return "VIERNES"


def add_days(date: str, days: int) -> str:
    """
    Adds given date, the given days
    :param date:
    :param days:
    :return: str
    """
    date_converted = datetime.strptime(date, "%d/%m/%y")
    date_add = date_converted + timedelta(days=days)

    return date_add.strftime("%d/%m/%y")


def add_days_return_datetime(date: str, days: int) -> datetime:
    """
    Adds given date, the given days
    :param date:
    :param days:
    :return: datetime
    """
    date_converted = datetime.strptime(date, "%d/%m/%y")
    date_add = date_converted + timedelta(days=days)

    return date_add
