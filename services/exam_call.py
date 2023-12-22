from datetime import datetime, timedelta
from typing import Tuple, List, Any

import numpy as np
import pandas as pd
from pandas import DataFrame

from model.materia import Materia
from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade, remove_accents
from utils.common.util import *


class ExamCall:
    first_year_result = pd.DataFrame(
        columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
    second_year_result = pd.DataFrame(
        columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
    third_year_result = pd.DataFrame(
        columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
    fourth_year_result = pd.DataFrame(
        columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
    fifth_year_result = pd.DataFrame(
        columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])

    first_year: tuple
    second_year: tuple
    third_year: tuple
    fourth_year: tuple
    fifth_year: tuple

    def __init__(self, df: DataFrame, period: dict):
        self.df = df
        self.period = period
        self.grade_1 = divide_dataframe_in_grade(self.df)[0]
        self.grade_2 = divide_dataframe_in_grade(self.df)[1]
        self.grade_3 = divide_dataframe_in_grade(self.df)[2]
        self.grade_4 = divide_dataframe_in_grade(self.df)[3]
        self.grade_5 = divide_dataframe_in_grade(self.df)[4]
        self.career_name = self.period["career_name"]

    def get_name_career(self) -> str:
        career_name = None
        name = remove_accents(self.career_name).lower()
        if name.startswith("kin"):
            career_name = "kinesiologia"
        elif name.startswith("nutri"):
            career_name = "nutricion"
        return career_name

    def get_central_subject_of_career(self) -> str | None:
        career_name = self.get_name_career()
        if career_name == "kinesiologia":
            return "TECNICAS KINESICAS "
        else:
            return None

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

    def get_list_of_dates(self) -> tuple[list[str], list[str]]:
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

    def get_first_and_second_year_filters_first_call(self, materias, valid_dates) -> tuple:
        count = 0
        result = pd.DataFrame(columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
        while len(materias) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for materia in materias:
                correlativa = materia.num_corr

                fecha_asignada = None

                for fecha in valid_dates:
                    if get_day_of_the_week(fecha) == materia.dia_1:
                        if fecha not in result['primer llamado'].values:
                            if (correlativa in ("0", "1") or
                                    len([mat.nombre for mat in materias if mat.nombre == materia.nombre]) == 1):
                                if fecha_asignada is None or fecha < fecha_asignada:
                                    fecha_asignada = fecha
                                    break
                            else:
                                if materia.nombre in result["materia"].values:
                                    get_fila = result.loc[
                                        result["materia"].values == materia.nombre]
                                    if pd.to_numeric(get_fila["correlativa num"].values[0]) < int(materia.num_corr):
                                        if fecha_asignada is None:
                                            fecha_posible = add_days(str(get_fila["primer llamado"].values[0]), 5)
                                            if fecha_posible in valid_dates and get_day_of_the_week(fecha_posible) in (
                                                    materia.dia_1, materia.dia_2):
                                                fecha_asignada = fecha_posible
                                                break
                                            else:
                                                while (fecha_posible in result['primer llamado'].values
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
                    result = result._append(
                        {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                         'primer llamado': fecha_asignada}, ignore_index=True)

                    materias.remove(materia)
                    valid_dates.remove(fecha_asignada)
                    break

        while len(materias) >= 1:
            for materia in materias:
                result = result._append(
                    {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                     'primer llamado': "None"}, ignore_index=True)

                materias.remove(materia)

        return valid_dates, result

    def get_third_and_fourth_year_filters_first_call(self, materias, valid_dates, central_materia,
                                                     last_date_materia) -> tuple:
        """
        only for kinesiologia
        :param materias: list of object Materia
        :param valid_dates: list of string
        :param central_materia: str
        :param last_date_materia:
        :return: tuple
        """
        count = 0
        result = pd.DataFrame(columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
        while len(materias) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for materia in materias:
                correlativa = materia.num_corr

                fecha_asignada = None

                for fecha in valid_dates:
                    if get_day_of_the_week(fecha) == materia.dia_1:
                        if fecha not in result['primer llamado'].values:
                            if correlativa in ("0", "1", "3", "5", "7") and materia.nombre != central_materia:
                                if fecha_asignada is None or fecha < fecha_asignada:
                                    fecha_asignada = fecha
                                    break
                            elif materia.nombre in result["materia"].values:
                                get_fila = result.loc[
                                    result["materia"].values == materia.nombre]
                                if pd.to_numeric(get_fila["correlativa num"].values[0]) < int(materia.num_corr):
                                    if fecha_asignada is None:
                                        fecha_posible = add_days(str(get_fila["primer llamado"].values[0]), 5)
                                        if fecha_posible in valid_dates and get_day_of_the_week(fecha_posible) in (
                                                materia.dia_1, materia.dia_2):
                                            fecha_asignada = fecha_posible
                                            break
                                        else:
                                            while (fecha_posible in result['primer llamado'].values
                                                   or fecha_posible not in valid_dates or get_day_of_the_week(
                                                        fecha_posible) != materia.dia_1):
                                                fecha_posible = add_days(fecha_posible, 1)
                                            fecha_asignada = fecha_posible
                                            break
                            elif materia.nombre == central_materia:
                                if fecha > last_date_materia:
                                    fecha_asignada = fecha
                                    break
                                else:
                                    fecha_posible = fecha
                                    while fecha_posible < last_date_materia or fecha_posible not in valid_dates or get_day_of_the_week(
                                            fecha_posible) not in (materia.dia_1, materia.dia_2):
                                        fecha_posible = add_days(fecha_posible, 1)
                                        if fecha_posible > self.period["end_date_first_period"]:
                                            break
                                    if fecha_posible <= self.period["end_date_first_period"]:
                                        fecha_asignada = fecha_posible
                                        break
                                    break
                        else:
                            continue
                    else:
                        continue

                if fecha_asignada:
                    result = result._append(
                        {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                         'primer llamado': fecha_asignada}, ignore_index=True)

                    materias.remove(materia)
                    valid_dates.remove(fecha_asignada)
                    break

        while len(materias) >= 1:
            for materia in materias:
                result = result._append(
                    {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                     'primer llamado': "None"}, ignore_index=True)

                materias.remove(materia)

        return valid_dates, result

    def create_first_call(self) -> tuple[tuple, tuple, tuple, tuple, tuple]:
        central_materia = self.get_central_subject_of_career()
        for grade in range(1, 6):
            if grade == 1:
                dates = self.get_list_of_dates()[0]
                materias_assign = self.create_materia_objects(1)
                empty_dates, self.first_year_result = self.get_first_and_second_year_filters_first_call(
                    materias=materias_assign,
                    valid_dates=dates)
                self.first_year = self.first_year_result, empty_dates
            elif grade == 2:
                dates = self.get_list_of_dates()[0]
                materias_assign = self.create_materia_objects(2)
                empty_dates, self.second_year_result = self.get_first_and_second_year_filters_first_call(
                    materias=materias_assign,
                    valid_dates=dates)
                self.second_year = self.second_year_result, empty_dates
            if grade == 3:
                dates = self.get_list_of_dates()[0]
                materias_assign = self.create_materia_objects(3)
                if self.get_name_career() == "nutricion":
                    empty_dates, self.third_year_result = self.get_first_and_second_year_filters_first_call(
                        materias=materias_assign,
                        valid_dates=dates)
                    self.third_year = self.third_year_result, empty_dates
                else:
                    get_fila = self.second_year_result.loc[self.second_year_result["materia"].values == central_materia]
                    get_last_call_materia = get_fila.sort_values(by=["correlativa num"], ascending=False)
                    last_date_materia = get_last_call_materia["primer llamado"].values[0]
                    empty_dates, self.third_year_result = self.get_third_and_fourth_year_filters_first_call(
                        materias=materias_assign,
                        valid_dates=dates,
                        central_materia=central_materia,
                        last_date_materia=last_date_materia)
                    self.third_year = self.third_year_result, empty_dates
            elif grade == 4:
                dates = self.get_list_of_dates()[0]
                materias_assign = self.create_materia_objects(4)
                if self.get_name_career() == "nutricion":
                    empty_dates, self.fourth_year_result = self.get_first_and_second_year_filters_first_call(
                        materias=materias_assign,
                        valid_dates=dates)
                    self.fourth_year = self.fourth_year_result, empty_dates
                else:
                    get_fila = self.third_year_result.loc[self.third_year_result["materia"].values == central_materia]
                    get_last_call_materia = get_fila.sort_values(by=["correlativa num"], ascending=False)
                    last_date_materia = get_last_call_materia["primer llamado"].values[0]
                    empty_dates, self.fourth_year_result = self.get_third_and_fourth_year_filters_first_call(
                        materias=materias_assign,
                        valid_dates=dates,
                        central_materia=central_materia,
                        last_date_materia=last_date_materia)
                    self.fourth_year = self.fourth_year_result,empty_dates
            elif grade == 5:
                dates = self.get_list_of_dates()[0]
                materias_assign = self.create_materia_objects(5)
                empty_dates, self.fifth_year_result = self.get_first_and_second_year_filters_first_call(
                    materias=materias_assign,
                    valid_dates=dates)
                self.fifth_year = self.fifth_year_result, empty_dates

        return self.first_year, self.second_year, self.third_year, self.fourth_year, self.fifth_year

    def get_second_call(self, materias, valid_dates, year_result, central_materia=None) -> tuple:
        count = 0

        while len(materias) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for materia in materias:
                correlativa = materia.num_corr

                fecha_asignada = None

                for fecha in valid_dates:
                    if get_day_of_the_week(fecha) in (materia.dia_1, materia.dia_2):
                        get_fila = year_result.loc[year_result["materia"].values == materia.nombre]
                        if len(get_fila) > 1:
                            get_fila = get_fila.loc[year_result["correlativa num"] == correlativa]
                        if get_fila["primer llamado"].values[0] == "None":
                            break
                        if datetime.strptime(fecha, '%d/%m/%y') >= add_days_return_datetime(
                                get_fila["primer llamado"].values[0], 7):
                            if correlativa in ("0", "1", "3", "5", "7") and materia.nombre != central_materia:
                                if fecha_asignada is None or fecha < fecha_asignada:
                                    fecha_asignada = fecha
                                    break
                            else:
                                get_fila = year_result.loc[year_result["materia"].values == materia.nombre]
                                if (type(get_fila["segundo llamado"].values[0]) == str and pd.to_numeric(
                                        get_fila["correlativa num"].values[0]) < int(materia.num_corr)):
                                    if fecha_asignada is None:
                                        if datetime.strptime(fecha, '%d/%m/%y') >= add_days_return_datetime(
                                                get_fila["segundo llamado"].values[0], 5):
                                            fecha_asignada = fecha
                                            break
                                        else:
                                            continue
                                else:
                                    continue
                        else:
                            continue

                if fecha_asignada:
                    year_result.loc[(year_result["materia"] == materia.nombre) & (
                            year_result["correlativa num"] == correlativa), "segundo llamado"] = fecha_asignada
                    materias.remove(materia)
                    valid_dates.remove(fecha_asignada)
                    break

        while len(materias) >= 1:
            for materia in materias:
                correlativa = materia.num_corr
                year_result.loc[(year_result["materia"] == materia.nombre) & (
                        year_result["correlativa num"] == correlativa), "segundo llamado"] = "None"
                materias.remove(materia)
                break

        empty_dates = valid_dates
        return empty_dates, year_result

    def create_second_call(self) -> tuple:
        self.create_first_call()
        central_materia = self.get_central_subject_of_career()
        for grade in range(1, 6):
            if grade == 1:
                empty_dates = self.first_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(key=lambda date: datetime.strptime(date, '%d/%m/%y'), reverse=False)
                materias_assign = self.create_materia_objects(1)
                empty_dates, self.first_year_result = self.get_second_call(
                    materias=materias_assign,
                    valid_dates=dates,
                    year_result=self.first_year_result)
                self.first_year = self.first_year_result, empty_dates
            elif grade == 2:
                empty_dates = self.second_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(key=lambda date: datetime.strptime(date, '%d/%m/%y'), reverse=False)
                materias_assign = self.create_materia_objects(2)
                empty_dates, self.second_year_result = self.get_second_call(
                    materias=materias_assign,
                    valid_dates=dates,
                    year_result=self.second_year_result)
                self.second_year = self.second_year_result, empty_dates
            if grade == 3:
                empty_dates = self.third_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(key=lambda date: datetime.strptime(date, '%d/%m/%y'), reverse=False)
                materias_assign = self.create_materia_objects(3)
                empty_dates, self.third_year_result = self.get_second_call(
                    materias=materias_assign,
                    valid_dates=dates,
                    year_result=self.third_year_result,
                    central_materia=central_materia)
                self.third_year = self.third_year_result, empty_dates
            elif grade == 4:
                empty_dates = self.fourth_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(key=lambda date: datetime.strptime(date, '%d/%m/%y'), reverse=False)
                materias_assign = self.create_materia_objects(4)
                empty_dates, self.fourth_year_result = self.get_second_call(
                    materias=materias_assign,
                    valid_dates=dates,
                    year_result=self.fourth_year_result,
                    central_materia=central_materia)
                self.fourth_year = self.fourth_year_result, empty_dates
            if grade == 5:
                empty_dates = self.fifth_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(key=lambda date: datetime.strptime(date, '%d/%m/%y'), reverse=False)
                materias_assign = self.create_materia_objects(5)
                empty_dates, self.fifth_year_result = self.get_second_call(
                    materias=materias_assign,
                    valid_dates=dates,
                    year_result=self.fifth_year_result,
                    central_materia=central_materia)
                self.fifth_year = self.fifth_year_result, empty_dates
        return self.first_year, self.second_year, self.third_year, self.fourth_year, self.fifth_year
