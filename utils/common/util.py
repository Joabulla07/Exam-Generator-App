from datetime import datetime, timedelta


def get_day_of_the_week(date: str) -> str:
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
    date_converted = datetime.strptime(date, "%d/%m/%y")
    date_add = date_converted + timedelta(days=days)

    return date_add.strftime("%d/%m/%y")


def add_days_return_datetime(date: str, days: int) -> datetime:
    date_converted = datetime.strptime(date, "%d/%m/%y")
    date_add = date_converted + timedelta(days=days)

    return date_add
