import pandas as pd
import pytest


@pytest.fixture
def expected_valid_dates():
    return (['02/02/24', '05/02/24', '06/02/24',
             '07/02/24', '08/02/24', '09/02/24',
             '14/02/24', '15/02/24', '16/02/24',
             '19/02/24', '20/02/24'],
            ['26/02/24', '27/02/24', '28/02/24',
             '29/02/24', '01/03/24', '04/03/24',
             '05/03/24', '06/03/24', '07/03/24',
             '08/03/24'])


@pytest.fixture
def get_period():
    return {"start_date_first_period": "02/02/24",
            "end_date_first_period": "20/02/24",
            "start_date_second_period": "26/02/24",
            "end_date_second_period": "08/03/24",
            "career_name": "kinesiologia"}


@pytest.fixture
def get_dataframe():
    data = {"GRADO": [1, 2, 2, 3, 4, 5],
            "MATERIA": ["Inglés Médico 1", "Química Biolóica 1", "Evaluaciones Kinefisiatricas",
                        "Técnicas Kinésicas 1", "Kinesiología Deportiva", "Práctica Clínica Guiada 1"],
            "DIA": ["lunes", "martes", "miércoles", "jueves", "viernes", "lunes"],
            "SEGUNDO_DIA": ["None", "jueves", "viernes", "lunes", "None", "None"]}
    return pd.DataFrame(data)
