import pandas as pd
import unicodedata
from pandas import DataFrame


def convert_excel_to_dataframe():
    df = pd.read_excel("../docs/materias.xlsx")
    return df


def divide_dataframe_in_grade(df) -> tuple:
    columns = df.columns.values.tolist()
    df.columns = [col.lower() for col in columns]
    df.materia = [mat.lower() for mat in df.materia]
    df["materia"] = df["materia"].apply(remove_accents)
    df.materia = [mat.upper() for mat in df.materia]
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


def sort_dataframe(df) -> DataFrame:
    return df.sort_values(by="materia")


def remove_accents(text) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
