import pytest

from utils.common.validation_utils import *


@pytest.mark.unit
def test_validate_date_ok():
    date = "18/12/23"
    assert validate_date(date) is None


@pytest.mark.unit
def test_validate_date_invalid():
    date = "1111"
    with pytest.raises(Exception) as e:
        validate_date(date)

    assert e.type == ValueError


@pytest.mark.unit
def test_validate_start_date_and_today_true():
    date = "10/12/33"
    assert validate_start_date_and_today(date) is True


@pytest.mark.unit
def test_validate_start_date_and_today_false():
    date = "10/10/20"
    assert validate_start_date_and_today(date) is False


@pytest.mark.unit
def test_validate_date_end_true():
    end_date = "15/12/23"
    start_date = "10/12/23"
    assert validate_date_end(end_date, start_date) is True


@pytest.mark.unit
def test_validate_date_end_false():
    end_date = "09/12/23"
    start_date = "10/12/23"
    assert validate_date_end(end_date, start_date) is False


@pytest.mark.unit
def test_validate_date_is_not_holiday_or_weekend_true_monday():
    date = "11/12/23"  # monday
    assert validate_date_is_not_holiday_or_weekend(date) is True


@pytest.mark.unit
def test_validate_date_is_not_holiday_or_weekend_false_sunday():
    date = "10/12/23"  # sunday
    assert validate_date_is_not_holiday_or_weekend(date) is False


@pytest.mark.unit
def test_validate_date_is_not_holiday_or_weekend_false_holiday():
    date = "09/07/23"  # independence day
    assert validate_date_is_not_holiday_or_weekend(date) is False
