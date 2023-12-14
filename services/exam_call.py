from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame

from model.materia import Materia
from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade
from utils.common.util import *


class ExamCall:

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

    def get_list_of_dates(self) -> list:
        start_date = datetime.strptime(self.period['start_date_first_period'], '%d/%m/%y')
        end_date = datetime.strptime(self.period['end_date_first_period'], '%d/%m/%y')
        start_recess = datetime.strptime(self.period['start_recess_date'], '%d/%m/%y')
        end_recess = datetime.strptime(self.period['end_recess_date'], '%d/%m/%y')
        date_list = [(start_date + timedelta(days=d)).strftime("%d/%m/%y")
                     for d in range((end_date - start_date).days + 1)]

        date_recess_list = [(start_recess + timedelta(days=d)).strftime("%d/%m/%y")
                            for d in range((end_recess - start_recess).days + 1)]

        definity_date_list = []
        for dates in date_list:
            if validate_date_is_not_holiday_or_weekend(dates) and dates not in date_recess_list:
                definity_date_list.append(dates)
        return definity_date_list

    def create_materia_objects(self, grade: int) -> list:
        materia_objects = []
        df = self.get_df_from_grade(grade)
        for i in range(len(df)):
            if df.iloc[i]["materia"][-1].isnumeric():
                materia_objects.append(
                    Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], num_corr=df.iloc[i]["materia"][-1],
                            dia=df.iloc[i]["dia"]))
            else:
                materia_objects.append(Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], dia=df.iloc[i]["dia"]))

        materia_objects.sort(key=lambda materia: materia.num_corr)
        return materia_objects

    def create_first_call_first_period_first_year(self, grade):
        resultado = pd.DataFrame(columns=['grado', 'materia', 'correlativa num', 'primer llamado', 'segundo llamado'])
        materias = self.create_materia_objects(grade)
        valid_dates = self.get_list_of_dates()
        result_dic = []
        for materia in materias:
            correlativa = materia.num_corr

            fecha_asignada = None

            for fecha in valid_dates:
                if get_day_of_the_week(fecha) == materia.dia:
                    if (fecha not in resultado['primer llamado'].values
                            and fecha not in resultado['segundo llamado'].values):
                        if correlativa in ("None", "1"):
                            if fecha_asignada is None or fecha < fecha_asignada:
                                fecha_asignada = fecha
                                break
                        else:
                            if materia.nombre in resultado["materia"].values:
                                get_fila = resultado.loc[resultado["materia"].values == materia.nombre]
                                if pd.to_numeric(get_fila["correlativa num"].values[0]) < int(materia.num_corr):
                                    if fecha_asignada is None:
                                        fecha_posible = add_days(str(get_fila["primer llamado"].values[0]), 5)
                                        if fecha_posible in valid_dates:
                                            fecha_asignada = fecha_posible
                                            break
                                        else:
                                            while (fecha_posible in resultado['primer llamado'].values
                                                   or fecha_posible in resultado['segundo llamado'].values or
                                                    fecha_posible not in valid_dates):
                                                fecha_posible = add_days(fecha_posible, 1)
                                            fecha_asignada = fecha_posible
                                            break
                    else:
                        continue
                else:
                    continue

            if fecha_asignada:
                resultado = resultado._append(
                    {'grado': materia.grado, 'materia': materia.nombre, 'correlativa num': materia.num_corr,
                     'primer llamado': fecha_asignada,
                     'segundo llamado': add_days(fecha_asignada, 7)}, ignore_index=True)
                #ToDo el segundo llamado no corrobora las fechas y agrega 7 dias. Verificar esto
        print(resultado)
        return resultado
