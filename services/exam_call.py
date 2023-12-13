from datetime import datetime, timedelta

from pandas import DataFrame

from model.materia import Materia
from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade


class ExamCall:

    def __init__(self, df: DataFrame, period: dict):
        self.df = df
        self.period = period
        self.grade_1 = divide_dataframe_in_grade(self.df)[0]
        self.grade_2 = divide_dataframe_in_grade(self.df)[1]
        self.grade_3 = divide_dataframe_in_grade(self.df)[2]
        self.grade_4 = divide_dataframe_in_grade(self.df)[3]
        self.grade_5 = divide_dataframe_in_grade(self.df)[4]

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

        for i in range(len(df)):
            if df.iloc[i]["materia"][-1].isnumeric():
                materia_objects.append(
                    Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], num_corr=df.iloc[i]["materia"][-1],
                            dia=df.iloc[i]["dia"]))
            else:
                materia_objects.append(Materia(grado=grade, nombre=df.iloc[i]["materia"][:-1], dia=df.iloc[i]["dia"]))

        materia_objects.sort(key=lambda materia: materia.num_corr)
        return materia_objects

    def create_first_call_first_period_first_year(self):
        first_year = self.create_materia_objects(1)
        dates = self.get_list_of_dates()
        copy_dates = dates.copy()
        # schedule = dict(zip(dates, ["None"] * len(dates)))
        # for materias in first_year:
        #     if materias.num_corr == "1":
        #         for dates_sch in schedule:
        #             if schedule[dates_sch] == "None":
        #                 print(materias)
        #                 print(schedule[dates_sch])
        #                 schedule[dates_sch] = materias
        #                 break
        #     else:
        #         continue

        for materias in first_year:
            pass
