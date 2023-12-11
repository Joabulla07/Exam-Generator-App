import pandas as pd


def convert_excel_to_dataframe():
    df = pd.read_excel("../docs/materias.xlsx")
    return df


def divide_dataframe_in_grade(df):
    columns = df.columns.values.tolist()
    df.columns = [col.lower() for col in columns]
    groups = df.groupby(df.grado)
    grade_1 = groups.get_group(1)
    grade_2 = groups.get_group(2)
    grade_3 = groups.get_group(3)
    grade_4 = groups.get_group(4)
    grade_5 = groups.get_group(5)
    return (sort_dataframe(grade_1),
            sort_dataframe(grade_2),
            sort_dataframe(grade_3),
            sort_dataframe(grade_4),
            sort_dataframe(grade_5))


def sort_dataframe(df):
    return df.sort_values(by="materia")
