#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
from math import ceil, floor
from .config import COLUMNS, VALIDSCORE

# Values manipulations


def round_half_point(val):
    try:
        return 0.5 * ceil(2.0 * val)
    except ValueError:
        return val
    except TypeError:
        return val


def score_to_mark(x):
    """ Compute the mark

    if the item is leveled then the score is multiply by the score_rate
    otherwise it copies the score

    :param x: dictionnary with COLUMNS["is_leveled"], COLUMNS["score"] and COLUMNS["score_rate"] keys

    >>> d = {"Eleve":["E1"]*6 + ["E2"]*6,
    ...    COLUMNS["score_rate"]:[1]*2+[2]*2+[2]*2 + [1]*2+[2]*2+[2]*2,
    ...    COLUMNS["is_leveled"]:[0]*4+[1]*2 + [0]*4+[1]*2,
    ...    COLUMNS["score"]:[1, 0.33, 2, 1.5, 1, 3,   0.666, 1, 1.5, 1, 2, 3],
    ...    }
    >>> df = pd.DataFrame(d)
    >>> score_to_mark(df.loc[0])
    1.0
    >>> score_to_mark(df.loc[10])
    1.3333333333333333
    """
    # -1 is no answer
    if x[COLUMNS["score"]] == -1:
        return 0

    if x[COLUMNS["is_leveled"]]:
        if x[COLUMNS["score"]] not in [0, 1, 2, 3]:
            raise ValueError(f"The evaluation is out of range: {x[COLUMNS['score']]} at {x}")
        return round_half_point(x[COLUMNS["score"]] * x[COLUMNS["score_rate"]] / 3)

    if x[COLUMNS["score"]] > x[COLUMNS["score_rate"]]:
        raise ValueError(
            f"The score ({x['score']}) is greated than the rating scale ({x[COLUMNS['score_rate']]}) at {x}"
        )
    return x[COLUMNS["score"]]


def score_to_level(x):
    """ Compute the level (".",0,1,2,3).

    :param x: dictionnary with COLUMNS["is_leveled"], COLUMNS["score"] and COLUMNS["score_rate"] keys

    >>> d = {"Eleve":["E1"]*6 + ["E2"]*6,
    ...    COLUMNS["score_rate"]:[1]*2+[2]*2+[2]*2 + [1]*2+[2]*2+[2]*2,
    ...    COLUMNS["is_leveled"]:[0]*4+[1]*2 + [0]*4+[1]*2,
    ...    COLUMNS["score"]:[1, 0.33, np.nan, 1.5, 1, 3,   0.666, 1, 1.5, 1, 2, 3],
    ...    }
    >>> df = pd.DataFrame(d)
    >>> score_to_level(df.loc[0])
    3
    >>> score_to_level(df.loc[1])
    1
    >>> score_to_level(df.loc[2])
    'na'
    >>> score_to_level(df.loc[3])
    3
    >>> score_to_level(df.loc[5])
    3
    >>> score_to_level(df.loc[10])
    2
    """
    # negatives are no answer or negatives points
    if x[COLUMNS["score"]] <= -1:
        return np.nan

    if x[COLUMNS["is_leveled"]]:
        return int(x[COLUMNS["score"]])

    return int(ceil(x[COLUMNS["score"]] / x[COLUMNS["score_rate"]] * 3))


# DataFrame columns manipulations


def compute_mark(df):
    """ Add Mark column to df

    :param df: DataFrame with COLUMNS["score"], COLUMNS["is_leveled"] and COLUMNS["score_rate"] columns.

    >>> d = {"Eleve":["E1"]*6 + ["E2"]*6,
    ...    COLUMNS["score_rate"]:[1]*2+[2]*2+[2]*2 + [1]*2+[2]*2+[2]*2,
    ...    COLUMNS["is_leveled"]:[0]*4+[1]*2 + [0]*4+[1]*2,
    ...    COLUMNS["score"]:[1, 0.33, 2, 1.5, 1, 3,   0.666, 1, 1.5, 1, 2, 3],
    ...    }
    >>> df = pd.DataFrame(d)
    >>> compute_mark(df)
    0     1.00
    1     0.33
    2     2.00
    3     1.50
    4     0.67
    5     2.00
    6     0.67
    7     1.00
    8     1.50
    9     1.00
    10    1.33
    11    2.00
    dtype: float64
    """
    return df[[COLUMNS["score"], COLUMNS["is_leveled"], COLUMNS["score_rate"]]].apply(
        score_to_mark, axis=1
    )


def compute_level(df):
    """ Add Mark column to df

    :param df: DataFrame with COLUMNS["score"], COLUMNS["is_leveled"] and COLUMNS["score_rate"] columns.

    >>> d = {"Eleve":["E1"]*6 + ["E2"]*6,
    ...    COLUMNS["score_rate"]:[1]*2+[2]*2+[2]*2 + [1]*2+[2]*2+[2]*2,
    ...    COLUMNS["is_leveled"]:[0]*4+[1]*2 + [0]*4+[1]*2,
    ...    COLUMNS["score"]:[np.nan, 0.33, 2, 1.5, 1, 3,   0.666, 1, 1.5, 1, 2, 3],
    ...    }
    >>> df = pd.DataFrame(d)
    >>> compute_level(df)
    0     na
    1      1
    2      3
    3      3
    4      1
    5      3
    6      2
    7      3
    8      3
    9      2
    10     2
    11     3
    dtype: object
    """
    return df[[COLUMNS["score"], COLUMNS["is_leveled"], COLUMNS["score_rate"]]].apply(
        score_to_level, axis=1
    )


def compute_normalized(df):
    """ Compute the normalized mark (Mark / score_rate)

    :param df: DataFrame with "Mark" and COLUMNS["score_rate"] columns

    >>> d = {"Eleve":["E1"]*6 + ["E2"]*6,
    ...    COLUMNS["score_rate"]:[1]*2+[2]*2+[2]*2 + [1]*2+[2]*2+[2]*2,
    ...    COLUMNS["is_leveled"]:[0]*4+[1]*2 + [0]*4+[1]*2,
    ...    COLUMNS["score"]:[1, 0.33, 2, 1.5, 1, 3,   0.666, 1, 1.5, 1, 2, 3],
    ...    }
    >>> df = pd.DataFrame(d)
    >>> df["Mark"] = compute_marks(df)
    >>> compute_normalized(df)
    0     1.00
    1     0.33
    2     1.00
    3     0.75
    4     0.33
    5     1.00
    6     0.67
    7     1.00
    8     0.75
    9     0.50
    10    0.67
    11    1.00
    dtype: float64
    """
    return df[COLUMNS["mark"]] / df[COLUMNS["score_rate"]]


# Postprocessing question scores


def pp_q_scores(df):
    """ Postprocessing questions scores dataframe

    :param df: questions-scores dataframe
    :return: same data frame with mark, level and normalize columns
    """
    assign = {
        COLUMNS["mark"]: compute_mark,
        COLUMNS["level"]: compute_level,
        COLUMNS["normalized"]: compute_normalized,
    }
    return df.assign(**assign)


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
