import numpy as np
import pandas as pd


def _UserItemCrossJoin(df):
    """
    Get cross-join of all users and items
    
    Args:
        df (pd.DataFrame): Source dataframe.

    Returns:
        pd.DataFrame: Dataframe with crossjoins
    
    """
    
    crossjoin_list = []
    for user in df.USER.unique():
        for item in df.ITEM.unique():
            crossjoin_list.append([user, item])

    cross_join_df = pd.DataFrame(data=crossjoin_list, columns=["USER", "ITEM"])
    
    return cross_join_df
    

def _FilterBy(df, filter_by_df, filter_by_cols):
    """From the input DataFrame (df), remove the records whose target column (filter_by_cols) values are
    exist in the filter-by DataFrame (filter_by_df)

    Args:
        df (pd.DataFrame): Source dataframe.
        filter_by_df (pd.DataFrame): Filter dataframe.
        filter_by_cols (iterable of str): Filter columns.

    Returns:
        pd.DataFrame: Dataframe filtered by filter_by_df on filter_by_cols
    """

    return df.loc[
        ~df.set_index(filter_by_cols).index.isin(
            filter_by_df.set_index(filter_by_cols).index
        )
    ]

