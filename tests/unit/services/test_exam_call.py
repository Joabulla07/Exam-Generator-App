from unittest import mock
from unittest.mock import patch

import pytest

from model.materia import Materia
from services.exam_call import ExamCall

MODULE_PATH = "services.exam_call"


@pytest.mark.unit
def test_get_list_of_dates(expected_valid_dates, get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)

    mock.patch(f'{MODULE_PATH}.validate_date_is_not_holiday_or_weekend',
               return_value=True)
    result = exam.get_list_of_dates()

    expected_result = expected_valid_dates
    assert result == expected_result


@pytest.mark.unit
def test_get_create_materia_objects(get_period, get_dataframe):
    exam = ExamCall(get_dataframe, get_period)
    result = [Materia(grado=1,
                     nombre="INGLES MEDICO ",
                     num_corr="1",
                     dia_1="LUNES",
                      dia_2="NONE")].__repr__()

    patch.object(Materia, "__init__", side_effect=result)

    assert exam.create_materia_objects(1).__repr__() == result
