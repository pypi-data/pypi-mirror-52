from collections import defaultdict
from typing import Any, Dict

import numpy as np
import pandas as pd
import pandas_profiling
import seaborn as sns

from .text_tools import (
    character_distribution,
    contains_lowercase,
    contains_non_printable,
    contains_numbers,
    contains_punctuation,
    contains_uppercase,
    word_distribution,
)


def df_pairplot(df, columns=None, *args, **kwargs) -> Any:
    """Compute a pairplot of a dataframe.

    Args:
        df: the dataframe under consideration
        columns: an optionnal subet of the columns
        *args: positionnal arguments for the seaborn pairplot
        **kwargs: keywords arguments for the seaborn pairplot

    Returns:
        A pairplot graph

    """
    if columns is None:
        columns = df.columns.values

    return sns.pairplot(df[columns], *args, **kwargs)


def df_report(df: pd.DataFrame) -> None:
    """Display a report of a dataframe.

    Args:
        df: the dataframe underconsideration

    Effects:
        Display a report about the dataset

    """
    return pandas_profiling.ProfileReport(df)


def analyze_text_column(df: pd.DataFrame, column_name: str) -> Dict[str, Any]:
    contains_upper = False
    contains_lower = False
    str_contains_numbers = False
    str_contains_punctuation = False
    str_contains_non_printable = False
    distribution = {
        "digits": 0,
        "upper": 0,
        "lower": 0,
        "punctuation": 0,
        "whitespace": 0,
        "others": 0,
    }
    word_distrib = defaultdict(lambda: 0)

    for text in df[column_name]:
        if isinstance(text, str):
            if not contains_upper:
                contains_upper = contains_uppercase(text)

            if not contains_lower:
                contains_lower = contains_lowercase(text)

            if not str_contains_numbers:
                str_contains_numbers = contains_numbers(text)

            if not str_contains_punctuation:
                str_contains_punctuation = contains_punctuation(text)

            if not str_contains_non_printable:
                str_contains_non_printable = contains_non_printable(text)

            sentence_distrib = character_distribution(text)
            for key in sentence_distrib:
                distribution[key] += sentence_distrib[key]

            sentence_word_distrib = word_distribution(text)
            for key in sentence_word_distrib:
                word_distrib[key] += sentence_word_distrib[key]

    total_chars = sum(distribution.values())
    values = np.array(list(word_distrib.values()))
    return {
        "contains_upper": contains_upper,
        "contains_lower": contains_lower,
        "contains_numbers": str_contains_numbers,
        "contains_punctuation": str_contains_punctuation,
        "contains_non_printable": str_contains_non_printable,
        "character_distribution": {k: v / total_chars for k, v in distribution.items()},
        "word_distribution": {
            "number_of_words": len(word_distrib),
            "min": np.min(values),
            "25%": np.quantile(values, 0.25),
            "mean": np.mean(values),
            "median": np.median(values),
            "75%": np.quantile(values, 0.75),
            "max": np.max(values),
        },
    }
