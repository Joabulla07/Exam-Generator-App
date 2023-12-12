from datetime import datetime, timedelta

from utils.common.validation_utils import validate_date_is_not_holiday_or_weekend
from utils.model.dataframe_utils import divide_dataframe_in_grade


class ExamCall:

    def __init__(self, df, period):
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
        date_list = [(start_date + timedelta(days=d)).strftime("%d/%m/%y")
                     for d in range((end_date - start_date).days + 1)]
        definity_date_list = []
        for dates in date_list:
            if validate_date_is_not_holiday_or_weekend(dates):
                definity_date_list.append(dates)
        return definity_date_list

    def create_first_year_call_first_period(self):
        date_dic = {}
        date_list = self.get_list_of_dates()
        print(date_list)
