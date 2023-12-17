from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame

from model.materia import Materia
from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade
from utils.common.util import *


class ExamCall:
    resultado = pd.DataFrame(columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])

    def __init__(self, df: DataFrame, period: dict):
        self.df = df
        self.period = period
        self.grade_1 = divide_dataframe_in_grade(self.df)[0]
        self.grade_2 = divide_dataframe_in_grade(self.df)[1]
        self.grade_3 = divide_dataframe_in_grade(self.df)[2]
        self.grade_4 = divide_dataframe_in_grade(self.df)[3]
        self.grade_5 = divide_dataframe_in_grade(self.df)[4]

    def get_df_from_grade(self, grade):
        if grade == 1:
            df = self.grade_1
        elif grade == 2:
            df = self.grade_2
        elif grade == 3:
            df = self.grade_3
        elif grade == 4:
            df = self.grade_4
        else:
            df = self.grade_5

        return df

    def get_list_of_dates(self) -> tuple:
        start_date = datetime.strptime(self.period['start_date_first_period'], '%d/%m/%y')
        end_date = datetime.strptime(self.period['end_date_first_period'], '%d/%m/%y')
        start_second_period = datetime.strptime(self.period['start_date_second_period'], '%d/%m/%y')
        end_second_period = datetime.strptime(self.period['end_date_second_period'], '%d/%m/%y')

        date_list_first_period = [(start_date + timedelta(days=d)).strftime("%d/%m/%y")
                                  for d in range((end_date - start_date).days + 1)]

        date_list_second_period = [(start_second_period + timedelta(days=d)).strftime("%d/%m/%y")
                                   for d in range((end_second_period - start_second_period).days + 1)]

        first_definity_date_list = []
        second_definity_date_list = []

        for dates in date_list_first_period:
            if validate_date_is_not_holiday_or_weekend(dates):
                first_definity_date_list.append(dates)

        for dates in date_list_second_period:
            if validate_date_is_not_holiday_or_weekend(dates):
                second_definity_date_list.append(dates)

        return first_definity_date_list, second_definity_date_list

    def create_materia_objects(self, grade: int) -> list:
        materia_objects = []
        df = self.get_df_from_grade(grade)
        for i in range(len(df)):
            if df.iloc[i]["materia"][-1].isnumeric():
                materia_objects.append(
                    Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], num_corr=df.iloc[i]["materia"][-1],
                            dia_1=df.iloc[i]["dia"], dia_2=df.iloc[i]["segundo_dia"]))
            else:
                materia_objects.append(Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], dia_1=df.iloc[i]["dia"]
                                               , dia_2=df.iloc[i]["segundo_dia"]))

        # materia_objects.sort(key=lambda materia: materia.num_corr)
        return materia_objects

    def create_first_call_period_first_and_second_year(self, grade):

        materias_assign = self.create_materia_objects(grade)
        materias = materias_assign.copy()
        dates = self.get_list_of_dates()[0]
        valid_dates = dates.copy()

        while len(materias) > 0 and len(valid_dates) > 0:
            for materia in materias:
                correlativa = materia.num_corr

                fecha_asignada = None

                for fecha in valid_dates:
                    if get_day_of_the_week(fecha) == materia.dia_1:
                        if fecha not in self.resultado['primer llamado'].values:
                            if (correlativa in ("0", "1") or
                                    len([mat.nombre for mat in materias if mat.nombre == materia.nombre]) == 1):
                                if fecha_asignada is None or fecha < fecha_asignada:
                                    fecha_asignada = fecha
                                    break
                            else:
                                if materia.nombre in self.resultado["materia"].values:
                                    get_fila = self.resultado.loc[self.resultado["materia"].values == materia.nombre]
                                    if pd.to_numeric(get_fila["correlativa num"].values[0]) < int(materia.num_corr):
                                        if fecha_asignada is None:
                                            fecha_posible = add_days(str(get_fila["primer llamado"].values[0]), 5)
                                            if fecha_posible in valid_dates and get_day_of_the_week(fecha_posible) in (
                                            materia.dia_1, materia.dia_2):
                                                fecha_asignada = fecha_posible
                                                break
                                            else:
                                                while (fecha_posible in self.resultado['primer llamado'].values
                                                       or fecha_posible not in valid_dates or get_day_of_the_week(
                                                            fecha_posible) != materia.dia_1):
                                                    fecha_posible = add_days(fecha_posible, 1)
                                                fecha_asignada = fecha_posible
                                                break
                        else:
                            continue
                    else:
                        continue

                if fecha_asignada:
                    self.resultado = self.resultado._append(
                        {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                         'primer llamado': fecha_asignada}, ignore_index=True)

                    materias.remove(materia)
                    valid_dates.remove(fecha_asignada)

        materias_without_date = materias
        empty_dates = valid_dates
        return self.resultado, materias_without_date, empty_dates


    # def create_second_call_period_first_and_second_year(self, grade):
    #     first_period, materias_without_date, empty_dates = self.create_first_call_period_first_and_second_year(grade)
