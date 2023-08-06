#!/usr/bin/env python
# encoding: utf-8

""" Extracting data from xlsx files """

import pandas as pd
from .config import NO_ST_COLUMNS, COLUMNS, VALIDSCORE

pd.set_option("Precision", 2)


def try_replace(x, old, new):
    try:
        return str(x).replace(old, new)
    except ValueError:
        return x


def extract_students(df, no_student_columns=NO_ST_COLUMNS.values()):
    """ Extract the list of students from df 

    :param df: the dataframe
    :param no_student_columns: columns that are not students
    :return: list of students
    """
    students = df.columns.difference(no_student_columns)
    return students


def flat_df_students(
    df, no_student_columns=NO_ST_COLUMNS.values(), postprocessing=True
):
    """ Flat the dataframe by returning a dataframe with on student on each line

    :param df: the dataframe (one row per questions)
    :param no_student_columns: columns that are not students
    :return: dataframe with one row per questions and students

    Columns of csv files:

    - NO_ST_COLUMNS meta data on questions
    - one for each students

    This function flat student's columns to "student" and "score"
    """
    students = extract_students(df, no_student_columns)
    scores = []
    for st in students:
        scores.append(
            pd.melt(
                df,
                id_vars=no_student_columns,
                value_vars=st,
                var_name=COLUMNS["student"],
                value_name=COLUMNS["score"],
            ).dropna(subset=[COLUMNS["score"]])
        )
    if postprocessing:
        return postprocess(pd.concat(scores))
    return pd.concat(scores)


def flat_df_for(
    df, student, no_student_columns=NO_ST_COLUMNS.values(), postprocessing=True
):
    """ Extract the data only for one student

    :param df: the dataframe (one row per questions)
    :param no_student_columns: columns that are not students
    :return: dataframe with one row per questions and students

    Columns of csv files:

    - NO_ST_COLUMNS meta data on questions
    - one for each students

    """
    students = extract_students(df, no_student_columns)
    if student not in students:
        raise KeyError("This student is not in the table")
    st_df = df[list(no_student_columns) + [student]]
    st_df = st_df.rename(columns={student: COLUMNS["score"]}).dropna(
        subset=[COLUMNS["score"]]
    )
    if postprocessing:
        return postprocess(st_df)
    return st_df


def postprocess(df):
    """ Postprocessing score dataframe 

    - Replace na with an empty string
    - Replace "NOANSWER" with -1
    - Turn commas number to dot numbers
    """

    df[COLUMNS["question"]].fillna("", inplace=True)
    df[COLUMNS["exercise"]].fillna("", inplace=True)
    df[COLUMNS["comment"]].fillna("", inplace=True)
    df[COLUMNS["competence"]].fillna("", inplace=True)

    df[COLUMNS["score"]] = pd.to_numeric(
        df[COLUMNS["score"]]
        .replace(VALIDSCORE["NOANSWER"], -1)
        .apply(lambda x: try_replace(x, ",", "."))
    )
    df[COLUMNS["score_rate"]] = pd.to_numeric(
        df[COLUMNS["score_rate"]].apply(lambda x: try_replace(x, ",", ".")),
        errors="coerce",
    )

    return df


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
