import unicodedata

import numpy as np
import pandas as pd
from pandas import DataFrame


def convert_excel_to_dataframe():
    df = pd.read_excel("../docs/kinesiologia.xlsx")
    df_2 = pd.read_excel("../docs/nutricion.xlsx")
    return df, df_2


def convert_dataframe_lower_upper_accent(df: DataFrame) -> DataFrame:
    """
    Remove accents from dataframe and convert them to uppercase
    :param df: DataFrame
    :return: DataFrame
    """
    columns = df.columns.values.tolist()
    df.columns = [remove_accents(col) for col in [col.lower() for col in columns]]
    df.materia = [mat.lower() for mat in df.materia]
    df.materia = df["materia"].apply(remove_accents)
    df.materia = [mat.upper() for mat in df.materia]
    df.dia = [d.lower() for d in df.dia]
    df.dia = df["dia"].apply(remove_accents)
    df.dia = [d.upper() for d in df.dia]

    for dias in df.segundo_dia:
        if dias in ("", " ", "nan", np.nan) or type(dias) == float:
            df.segundo_dia = "None"

    df.segundo_dia = [d.lower() for d in df.segundo_dia]
    df.segundo_dia = df["segundo_dia"].apply(remove_accents)
    df.segundo_dia = [d.upper() for d in df.segundo_dia]
    return df


def divide_dataframe_in_grade(df: DataFrame) -> tuple:
    """
    Create five different Dataframe for the original Dataframe by grade
    :param df: DataFrame
    :return: tuple od DataFrames
    """
    df = convert_dataframe_lower_upper_accent(df)
    groups = df.groupby(df.grado)
    grade_1 = groups.get_group(1)
    grade_2 = groups.get_group(2)
    grade_3 = groups.get_group(3)
    grade_4 = groups.get_group(4)
    grade_5 = groups.get_group(5)
    return grade_1, grade_2, grade_3, grade_4, grade_5


def sort_dataframe(df: DataFrame) -> DataFrame:
    """
    sort the DataFrame by the column materia
    :param df: DataFrame
    :return: DataFrame
    """
    return df.sort_values(by="materia")


def remove_accents(text: str) -> str:
    """
    remove accents from a string
    :param text: str
    :return: str
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
