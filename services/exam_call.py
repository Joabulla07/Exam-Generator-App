import pandas as pd
from pandas import DataFrame

from model.materia import Subject
from utils.common.util import *
from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade


class ExamCall:
    first_year_result = pd.DataFrame(
        columns=[
            "grado",
            "materia",
            "correlativa num",
            "primer llamado",
            "segundo llamado",
        ]
    )
    second_year_result = pd.DataFrame(
        columns=[
            "grado",
            "materia",
            "correlativa num",
            "primer llamado",
            "segundo llamado",
        ]
    )
    third_year_result = pd.DataFrame(
        columns=[
            "grado",
            "materia",
            "correlativa num",
            "primer llamado",
            "segundo llamado",
        ]
    )
    fourth_year_result = pd.DataFrame(
        columns=[
            "grado",
            "materia",
            "correlativa num",
            "primer llamado",
            "segundo llamado",
        ]
    )
    fifth_year_result = pd.DataFrame(
        columns=[
            "grado",
            "materia",
            "correlativa num",
            "primer llamado",
            "segundo llamado",
        ]
    )

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

    def get_central_subject_of_career(self) -> str | None:
        """
        get the central subject of the career
        :return: str
        """
        if self.career_name == "kinesiologia":
            return "TECNICAS KINESICAS "
        else:
            return None

    def get_df_from_grade(self, grade) -> DataFrame:
        """
        get the corresponding dataframe for grade
        :param grade:
        :return: DataFrame
        """
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
        """
        get the list of the available dates for exam calls
        :return: tuple[list[str], list[str]]
        """
        start_date = datetime.strptime(
            self.period["start_date_first_period"], "%d/%m/%y"
        )
        end_date = datetime.strptime(self.period["end_date_first_period"], "%d/%m/%y")
        start_second_period = datetime.strptime(
            self.period["start_date_second_period"], "%d/%m/%y"
        )
        end_second_period = datetime.strptime(
            self.period["end_date_second_period"], "%d/%m/%y"
        )

        date_list_first_period = [
            (start_date + timedelta(days=d)).strftime("%d/%m/%y")
            for d in range((end_date - start_date).days + 1)
        ]

        date_list_second_period = [
            (start_second_period + timedelta(days=d)).strftime("%d/%m/%y")
            for d in range((end_second_period - start_second_period).days + 1)
        ]

        first_definity_date_list = []
        second_definity_date_list = []

        for dates in date_list_first_period:
            if validate_date_is_not_holiday_or_weekend(dates):
                first_definity_date_list.append(dates)

        for dates in date_list_second_period:
            if validate_date_is_not_holiday_or_weekend(dates):
                second_definity_date_list.append(dates)

        return first_definity_date_list, second_definity_date_list

    def create_subject_objects(self, grade: int) -> list:
        """
        Creates Subject Objects with the corresponding Data
        :param grade:
        :return: list of Subject Objects
        """
        subject_objects = []
        df = self.get_df_from_grade(grade)
        for i in range(len(df)):
            if df.iloc[i]["materia"][-1].isnumeric():
                subject_objects.append(
                    Subject(
                        grade=grade,
                        subject_name=df.iloc[i]["materia"][:-1],
                        correlative_number=df.iloc[i]["materia"][-1],
                        day_1=df.iloc[i]["dia"],
                        day_2=df.iloc[i]["segundo_dia"],
                    )
                )
            else:
                subject_objects.append(
                    Subject(
                        grade=grade,
                        subject_name=df.iloc[i]["materia"][:-1],
                        day_1=df.iloc[i]["dia"],
                        day_2=df.iloc[i]["segundo_dia"],
                    )
                )

        return subject_objects

    def get_first_and_second_year_filters_first_call(
        self, subjects, valid_dates
    ) -> tuple:
        """
        Generate first & second year exam calls for all subjects
        :param subjects:
        :param valid_dates:
        :return: tuple with results and dates without subject
        """
        count = 0
        result = pd.DataFrame(
            columns=[
                "grado",
                "materia",
                "correlativa num",
                "primer llamado",
                "segundo llamado",
            ]
        )
        while len(subjects) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for item in subjects:
                correlative = item.correlative_number

                assigned_date = None

                for date in valid_dates:
                    if get_day_of_the_week(date) == item.day_1:
                        if date not in result["primer llamado"].values:
                            if (
                                correlative in ("0", "1")
                                or len(
                                    [
                                        sub.subject_name
                                        for sub in subjects
                                        if sub.subject_name == item.subject_name
                                    ]
                                )
                                == 1
                            ):
                                if assigned_date is None or date < assigned_date:
                                    assigned_date = date
                                    break
                            else:
                                if item.subject_name in result["materia"].values:
                                    get_fila = result.loc[
                                        result["materia"].values == item.subject_name
                                    ]
                                    if pd.to_numeric(
                                        get_fila["correlativa num"].values[0]
                                    ) < int(item.correlative_number):
                                        if assigned_date is None:
                                            possible_date = add_days(
                                                str(
                                                    get_fila["primer llamado"].values[0]
                                                ),
                                                5,
                                            )
                                            if (
                                                possible_date in valid_dates
                                                and get_day_of_the_week(possible_date)
                                                in (item.day_1, item.day_2)
                                            ):
                                                assigned_date = possible_date
                                                break
                                            else:
                                                while (
                                                    possible_date
                                                    in result["primer llamado"].values
                                                    or possible_date not in valid_dates
                                                    or get_day_of_the_week(
                                                        possible_date
                                                    )
                                                    != item.day_1
                                                ):
                                                    possible_date = add_days(
                                                        possible_date, 1
                                                    )
                                                assigned_date = possible_date
                                                break
                        else:
                            continue
                    else:
                        continue

                if assigned_date:
                    result = result._append(
                        {
                            "grado": item.grade,
                            "materia": item.subject_name,
                            "correlativa num": item.correlative_number,
                            "primer llamado": assigned_date,
                        },
                        ignore_index=True,
                    )

                    subjects.remove(item)
                    valid_dates.remove(assigned_date)
                    break

        while len(subjects) >= 1:
            for item in subjects:
                result = result._append(
                    {
                        "grado": item.grade,
                        "materia": item.subject_name,
                        "correlativa num": item.correlative_number,
                        "primer llamado": "None",
                    },
                    ignore_index=True,
                )

                subjects.remove(item)

        return valid_dates, result

    def get_third_and_fourth_year_filters_first_call(
        self, subject, valid_dates, central_subject, last_date_subject
    ) -> tuple:
        """
        only for kinesiologia
        Generate third & fourth year exam calls for all subjects
        :param subject: list of object Subject
        :param valid_dates: list of string
        :param central_subject: str
        :param last_date_subject:
        :return: tuple
        """
        count = 0
        result = pd.DataFrame(
            columns=[
                "grado",
                "materia",
                "correlativa num",
                "primer llamado",
                "segundo llamado",
            ]
        )
        while len(subject) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for item in subject:
                correlative = item.correlative_number

                assigned_date = None

                for date in valid_dates:
                    if get_day_of_the_week(date) == item.day_1:
                        if date not in result["primer llamado"].values:
                            if (
                                correlative in ("0", "1", "3", "5", "7")
                                and item.subject_name != central_subject
                            ):
                                if assigned_date is None or date < assigned_date:
                                    assigned_date = date
                                    break
                            elif item.subject_name in result["materia"].values:
                                get_fila = result.loc[
                                    result["materia"].values == item.subject_name
                                ]
                                if pd.to_numeric(
                                    get_fila["correlativa num"].values[0]
                                ) < int(item.correlative_number):
                                    if assigned_date is None:
                                        possible_date = add_days(
                                            str(get_fila["primer llamado"].values[0]), 5
                                        )
                                        if (
                                            possible_date in valid_dates
                                            and get_day_of_the_week(possible_date)
                                            in (item.day_1, item.day_2)
                                        ):
                                            assigned_date = possible_date
                                            break
                                        else:
                                            while (
                                                possible_date
                                                in result["primer llamado"].values
                                                or possible_date not in valid_dates
                                                or get_day_of_the_week(possible_date)
                                                != item.day_1
                                            ):
                                                possible_date = add_days(
                                                    possible_date, 1
                                                )
                                            assigned_date = possible_date
                                            break
                            elif item.subject_name == central_subject:
                                if date > last_date_subject:
                                    assigned_date = date
                                    break
                                else:
                                    possible_date = date
                                    while (
                                        possible_date < last_date_subject
                                        or possible_date not in valid_dates
                                        or get_day_of_the_week(possible_date)
                                        not in (item.day_1, item.day_2)
                                    ):
                                        possible_date = add_days(possible_date, 1)
                                        if (
                                            possible_date
                                            > self.period["end_date_first_period"]
                                        ):
                                            break
                                    if (
                                        possible_date
                                        <= self.period["end_date_first_period"]
                                    ):
                                        assigned_date = possible_date
                                        break
                                    break
                        else:
                            continue
                    else:
                        continue

                if assigned_date:
                    result = result._append(
                        {
                            "grado": item.grade,
                            "materia": item.subject_name,
                            "correlativa num": item.correlative_number,
                            "primer llamado": assigned_date,
                        },
                        ignore_index=True,
                    )

                    subject.remove(item)
                    valid_dates.remove(assigned_date)
                    break

        while len(subject) >= 1:
            for item in subject:
                result = result._append(
                    {
                        "grado": item.grade,
                        "materia": item.subject_name,
                        "correlativa num": item.correlative_number,
                        "primer llamado": "None",
                    },
                    ignore_index=True,
                )

                subject.remove(item)

        return valid_dates, result

    def get_second_call(
        self, subject, valid_dates, year_result, central_subject=None
    ) -> tuple:
        """
        Generate second exam call
        :param subject:
        :param valid_dates:
        :param year_result:
        :param central_subject:
        :return: tuple with subjects with dates and dates without subject
        """
        count = 0

        while len(subject) > 0 and len(valid_dates) > 0 and count < 20:
            count = count + 1
            for item in subject:
                correlative = item.correlative_number

                assigned_date = None

                for date in valid_dates:
                    if get_day_of_the_week(date) in (item.day_1, item.day_2):
                        get_fila = year_result.loc[
                            year_result["materia"].values == item.subject_name
                        ]
                        if len(get_fila) > 1:
                            get_fila = get_fila.loc[
                                year_result["correlativa num"] == correlative
                            ]
                        if get_fila["primer llamado"].values[0] == "None":
                            break
                        if datetime.strptime(
                            date, "%d/%m/%y"
                        ) >= add_days_return_datetime(
                            get_fila["primer llamado"].values[0], 7
                        ):
                            if (
                                correlative in ("0", "1", "3", "5", "7")
                                and item.subject_name != central_subject
                            ):
                                if assigned_date is None or date < assigned_date:
                                    assigned_date = date
                                    break
                            else:
                                get_fila = year_result.loc[
                                    year_result["materia"].values == item.subject_name
                                ]
                                if type(
                                    get_fila["segundo llamado"].values[0]
                                ) == str and pd.to_numeric(
                                    get_fila["correlativa num"].values[0]
                                ) < int(
                                    item.correlative_number
                                ):
                                    if assigned_date is None:
                                        if datetime.strptime(
                                            date, "%d/%m/%y"
                                        ) >= add_days_return_datetime(
                                            get_fila["segundo llamado"].values[0], 5
                                        ):
                                            assigned_date = date
                                            break
                                        else:
                                            continue
                                else:
                                    continue
                        else:
                            continue

                if assigned_date:
                    year_result.loc[
                        (year_result["materia"] == item.subject_name)
                        & (year_result["correlativa num"] == correlative),
                        "segundo llamado",
                    ] = assigned_date
                    subject.remove(item)
                    valid_dates.remove(assigned_date)
                    break

        while len(subject) >= 1:
            for item in subject:
                correlative = item.correlative_number
                year_result.loc[
                    (year_result["materia"] == item.subject_name)
                    & (year_result["correlativa num"] == correlative),
                    "segundo llamado",
                ] = "None"
                subject.remove(item)
                break

        year_result = year_result._append(
            {
                "grado": "",
                "materia": valid_dates,
                "correlativa num": "",
                "primer llamado": "",
            },
            ignore_index=True,
        )

        return valid_dates, year_result

    def create_first_call(self) -> tuple[tuple, tuple, tuple, tuple, tuple]:
        """
        Creates first exam call.
        :return: Tuple with DataFrame and dates
        """
        central_subject = self.get_central_subject_of_career()
        for grade in range(1, 6):
            if grade == 1:
                dates = self.get_list_of_dates()[0]
                assign_subject = self.create_subject_objects(1)
                (
                    empty_dates,
                    self.first_year_result,
                ) = self.get_first_and_second_year_filters_first_call(
                    subjects=assign_subject, valid_dates=dates
                )
                self.first_year = self.first_year_result, empty_dates
            elif grade == 2:
                dates = self.get_list_of_dates()[0]
                assign_subject = self.create_subject_objects(2)
                (
                    empty_dates,
                    self.second_year_result,
                ) = self.get_first_and_second_year_filters_first_call(
                    subjects=assign_subject, valid_dates=dates
                )
                self.second_year = self.second_year_result, empty_dates
            if grade == 3:
                dates = self.get_list_of_dates()[0]
                assign_subject = self.create_subject_objects(3)
                if self.career_name == "nutricion":
                    (
                        empty_dates,
                        self.third_year_result,
                    ) = self.get_first_and_second_year_filters_first_call(
                        subjects=assign_subject, valid_dates=dates
                    )
                    self.third_year = self.third_year_result, empty_dates
                else:
                    get_fila = self.second_year_result.loc[
                        self.second_year_result["materia"].values == central_subject
                    ]
                    get_last_call_materia = get_fila.sort_values(
                        by=["correlativa num"], ascending=False
                    )
                    last_date_subject = get_last_call_materia["primer llamado"].values[
                        0
                    ]
                    (
                        empty_dates,
                        self.third_year_result,
                    ) = self.get_third_and_fourth_year_filters_first_call(
                        subject=assign_subject,
                        valid_dates=dates,
                        central_subject=central_subject,
                        last_date_subject=last_date_subject,
                    )
                    self.third_year = self.third_year_result, empty_dates
            elif grade == 4:
                dates = self.get_list_of_dates()[0]
                assign_subject = self.create_subject_objects(4)
                if self.career_name == "nutricion":
                    (
                        empty_dates,
                        self.fourth_year_result,
                    ) = self.get_first_and_second_year_filters_first_call(
                        subjects=assign_subject, valid_dates=dates
                    )
                    self.fourth_year = self.fourth_year_result, empty_dates
                else:
                    get_fila = self.third_year_result.loc[
                        self.third_year_result["materia"].values == central_subject
                    ]
                    get_last_call_subject = get_fila.sort_values(
                        by=["correlativa num"], ascending=False
                    )
                    last_date_subject = get_last_call_subject["primer llamado"].values[
                        0
                    ]
                    (
                        empty_dates,
                        self.fourth_year_result,
                    ) = self.get_third_and_fourth_year_filters_first_call(
                        subject=assign_subject,
                        valid_dates=dates,
                        central_subject=central_subject,
                        last_date_subject=last_date_subject,
                    )
                    self.fourth_year = self.fourth_year_result, empty_dates
            elif grade == 5:
                dates = self.get_list_of_dates()[0]
                assign_subject = self.create_subject_objects(5)
                (
                    empty_dates,
                    self.fifth_year_result,
                ) = self.get_first_and_second_year_filters_first_call(
                    subjects=assign_subject, valid_dates=dates
                )
                self.fifth_year = self.fifth_year_result, empty_dates

        return (
            self.first_year,
            self.second_year,
            self.third_year,
            self.fourth_year,
            self.fifth_year,
        )

    def create_second_call(self) -> None:
        """
        Create second exam call and generate all exams for all years
        :return: None
        """
        self.create_first_call()
        central_subject = self.get_central_subject_of_career()
        for grade in range(1, 6):
            if grade == 1:
                empty_dates = self.first_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(
                    key=lambda date: datetime.strptime(date, "%d/%m/%y"), reverse=False
                )
                assign_subject = self.create_subject_objects(1)
                empty_dates, self.first_year_result = self.get_second_call(
                    subject=assign_subject,
                    valid_dates=dates,
                    year_result=self.first_year_result,
                )

            elif grade == 2:
                empty_dates = self.second_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(
                    key=lambda date: datetime.strptime(date, "%d/%m/%y"), reverse=False
                )
                assign_subject = self.create_subject_objects(2)
                empty_dates, self.second_year_result = self.get_second_call(
                    subject=assign_subject,
                    valid_dates=dates,
                    year_result=self.second_year_result,
                )

            if grade == 3:
                empty_dates = self.third_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(
                    key=lambda date: datetime.strptime(date, "%d/%m/%y"), reverse=False
                )
                assign_subject = self.create_subject_objects(3)
                empty_dates, self.third_year_result = self.get_second_call(
                    subject=assign_subject,
                    valid_dates=dates,
                    year_result=self.third_year_result,
                    central_subject=central_subject,
                )

            elif grade == 4:
                empty_dates = self.fourth_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(
                    key=lambda date: datetime.strptime(date, "%d/%m/%y"), reverse=False
                )
                assign_subject = self.create_subject_objects(4)
                empty_dates, self.fourth_year_result = self.get_second_call(
                    subject=assign_subject,
                    valid_dates=dates,
                    year_result=self.fourth_year_result,
                    central_subject=central_subject,
                )

            if grade == 5:
                empty_dates = self.fifth_year[1]
                dates = self.get_list_of_dates()[1]
                [dates.append(date) for date in empty_dates]
                dates.sort(
                    key=lambda date: datetime.strptime(date, "%d/%m/%y"), reverse=False
                )
                assign_subject = self.create_subject_objects(5)
                empty_dates, self.fifth_year_result = self.get_second_call(
                    subject=assign_subject,
                    valid_dates=dates,
                    year_result=self.fifth_year_result,
                    central_subject=central_subject,
                )
