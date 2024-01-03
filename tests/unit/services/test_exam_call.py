from unittest import mock
from unittest.mock import patch

import pytest
from pandas import DataFrame

from model.materia import Subject
from services.exam_call import ExamCall

MODULE_PATH = "services.exam_call"


@pytest.mark.unit
def test_get_list_of_dates(expected_valid_dates, get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)

    mock.patch(
        f"{MODULE_PATH}.validate_date_is_not_holiday_or_weekend", return_value=True
    )
    result = exam.get_list_of_dates()

    expected_result = expected_valid_dates
    assert result == expected_result


@pytest.mark.unit
def test_get_create_subject_objects(get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)
    result = [
        Subject(
            grade=1,
            subject_name="INGLES MEDICO ",
            correlative_number="1",
            day_1="LUNES",
            day_2="NONE",
        )
    ].__repr__()

    patch.object(Subject, "__init__", side_effect=result)

    assert exam.create_subject_objects(1).__repr__() == result


@pytest.mark.unit
def test_get_central_subject_of_career_kinesiologia(get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)
    exam.career_name = "kinesiologia"
    assert exam.get_central_subject_of_career() == "TECNICAS KINESICAS "


@pytest.mark.unit
def test_get_central_subject_of_career_other_career(get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)
    exam.career_name = "otra_carrera"
    assert exam.get_central_subject_of_career() is None


@pytest.mark.unit
def test_get_df_from_grade(get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)
    assert isinstance(exam.get_df_from_grade(1), DataFrame)
    assert isinstance(exam.get_df_from_grade(2), DataFrame)
    assert isinstance(exam.get_df_from_grade(3), DataFrame)
    assert isinstance(exam.get_df_from_grade(4), DataFrame)
    assert isinstance(exam.get_df_from_grade(5), DataFrame)
    assert exam.get_df_from_grade(6) is None
