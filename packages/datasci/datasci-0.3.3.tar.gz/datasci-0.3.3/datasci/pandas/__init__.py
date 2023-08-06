from itertools import combinations
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def drop_na_columns(df: pd.DataFrame, inplace=False) -> pd.DataFrame:
    """
    Simply calls df.dropna(axis='columns', how='all', ...)
    """
    return df.dropna(axis='columns', how='all', inplace=inplace)


def drop_uninformative_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns from df where values in all cells are identical.
    """
    # TODO: support DataFrames where df.columns is a MultiIndex
    for column in df.columns:
        series = df[column]
        series_iter = iter(df[column])
        try:
            exemplar = next(series_iter)
        except StopIteration:
            # no rows => nothing to check :|
            continue
        # nan is a special case, since np.nan != np.nan
        if series.dtype == np.float and np.isnan(exemplar) and all(np.isnan(item) for item in series_iter):
            logger.debug('Dropping column %r from DataFrame (every value is nan)', column)
            df = df.drop(column, axis='columns')
        elif all(item == exemplar for item in series_iter):
            logger.debug('Dropping column %r from DataFrame (every value = %r)', column, exemplar)
            df = df.drop(column, axis='columns')
    return df


def drop_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns from df where values in all cells are identical to those in a preceding column.
    """
    for column1, column2 in combinations(df.columns, 2):
        if column1 not in df or column2 not in df:
            continue
        series1 = df[column1]
        series2 = df[column2]
        # convert dtypes to strings since numpy raises "TypeError: data type not understood"
        # when comparing to pandas's dtypes extensions
        if str(series1.dtype) == str(series2.dtype) and all(series1 == series2):
            logger.debug('Dropping column %r from DataFrame (duplicate of %r)', column2, column1)
            df = df.drop(column2, axis='columns')
    return df
