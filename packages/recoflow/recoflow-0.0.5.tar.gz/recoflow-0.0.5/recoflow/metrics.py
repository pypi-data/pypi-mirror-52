import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from .utils import _UserItemCrossJoin, _FilterBy

def _MergeRatingTruePred(rating_true, rating_pred):
  """Joins ground truth and predictions data frames on USER and ITEMS

  Params:
  rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
  rating_pred (pd.DataFrame): Predicated Ratings.

  Returns:
  np.array: Array with true ratings
  np.array: Array with predicted ratings
  """
  suffixes = ["_TRUE", "_PRED"]
  rating_true_pred = pd.merge(rating_true, rating_pred, on=["USER", "ITEM"], suffixes=suffixes)

  return rating_true_pred["RATING_TRUE"], rating_true_pred["RATING_PRED"]


def MeanSquaredError(rating_true, rating_pred):
  """Calculate Mean Squared Error
  
  Params:
  rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
  rating_pred (pd.DataFrame): Predicated Ratings.

  Returns:
  float: Mean Squared Error
  """

  y_true, y_pred = _MergeRatingTruePred(
    rating_true=rating_true, 
    rating_pred=rating_pred)
  
  return mean_squared_error(y_true, y_pred)


def RootMeanSquaredError(rating_true, rating_pred):
  """Calculate Root Mean Squared Error
  
  Params:
  rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
  rating_pred (pd.DataFrame): Predicated Ratings.

  Returns:
  float: Root Mean Squared Error
  """

  y_true, y_pred = _MergeRatingTruePred(
    rating_true=rating_true, 
    rating_pred=rating_pred)
  
  return np.sqrt(mean_squared_error(y_true, y_pred))


def MeanAbsoluteError(rating_true, rating_pred):
  """Calculate Mean Absolute Error
  
  Params:
  rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
  rating_pred (pd.DataFrame): Predicated Ratings.

  Returns:
  float: Mean Absolute Error
  """

  y_true, y_pred = _MergeRatingTruePred(
    rating_true=rating_true, 
    rating_pred=rating_pred)
  
  return mean_absolute_error(y_true, y_pred)



def _GetTopKItems(df, col_user, col_rating, k=10):
    """Get the top k items for each user.

    Params:
        dataframe (pandas.DataFrame): DataFrame of rating data
        col_user (str): column name for user
        col_rating (str): column name for rating
        k (int): number of items for each user

    Returns:
        pd.DataFrame: DataFrame of top k items for each user, sorted by `col_user` and `rank`
    """
    # Sort dataframe by col_user and (top k) col_rating
    top_k_items = (
        df.groupby(col_user, as_index=False)
        .apply(lambda x: x.nlargest(k, col_rating))
        .reset_index(drop=True)
    )
    # Add ranks
    top_k_items["rank"] = top_k_items.groupby(col_user, sort=False).cumcount() + 1
    return top_k_items




def _GetHitDF(rating_true, rating_pred, k):
    """Get Hit defined by relevancy, a hit usually means whether the recommended "k" items hit the "relevant" items by the user.
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    pd.DataFrame: Whether recommended K items hit the relevant item by user
    """    


    # Make sure the prediction and true data frames have the same set of users
    common_users = set(rating_true["USER"]).intersection(set(rating_pred["USER"]))
    rating_true_common = rating_true[rating_true["USER"].isin(common_users)]
    rating_pred_common = rating_pred[rating_pred["USER"].isin(common_users)]
    n_users = len(common_users)

    df_hit = _GetTopKItems(rating_pred_common, "USER", "RATING", k)
    df_hit = pd.merge(df_hit, rating_true_common, on=["USER", "ITEM"])[
        ["USER", "ITEM", "rank"]
    ]

    # count the number of hits vs actual relevant items per user
    df_hit_count = pd.merge(
        df_hit.groupby("USER", as_index=False)["USER"].agg({"hit": "count"}),
        rating_true_common.groupby("USER", as_index=False)["USER"].agg(
            {"actual": "count"}
        ),
        on="USER",
    )
    
    return df_hit, df_hit_count, n_users


def PrecisionK(rating_true, rating_pred, k=5):
    """Calculate Precision at K
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    float: Precision at K
    """

    df_hit, df_hit_count, n_users = _GetHitDF(rating_true, rating_pred, k)
    
    if df_hit.shape[0] == 0:
        return 0.0

    return (df_hit_count["hit"] / k).sum() / n_users


def RecallK(rating_true, rating_pred, k):
    """Calculate Precision at K
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    float: Recall at K
    """

    df_hit, df_hit_count, n_users = _GetHitDF(rating_true, rating_pred, k)

    if df_hit.shape[0] == 0:
        return 0.0

    return (df_hit_count["hit"] / df_hit_count["actual"]).sum() / n_users



def NDCGK(rating_true, rating_pred, k):
    """Calculate NDCG at K
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    float: NDCG at K
    """
    df_hit, df_hit_count, n_users = _GetHitDF(rating_true, rating_pred, k)
    
    if df_hit.shape[0] == 0:
        return 0.0

    # calculate discounted gain for hit items
    df_dcg = df_hit.copy()
    # relevance in this case is always 1
    df_dcg["dcg"] = 1 / np.log1p(df_dcg["rank"])
    # sum up discount gained to get discount cumulative gain
    df_dcg = df_dcg.groupby("USER", as_index=False, sort=False).agg({"dcg": "sum"})
    # calculate ideal discounted cumulative gain
    df_ndcg = pd.merge(df_dcg, df_hit_count, on=["USER"])
    df_ndcg["idcg"] = df_ndcg["actual"].apply(
        lambda x: sum(1 / np.log1p(range(1, min(x, k) + 1)))
    )

    # DCG over IDCG is the normalized DCG
    return (df_ndcg["dcg"] / df_ndcg["idcg"]).sum() / n_users


def MeanAveragePrecisionK(rating_true, rating_pred, k):
    """Calculate Mean Average Precision at K
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    float: Mean Average Precision at K
    """
    df_hit, df_hit_count, n_users = _GetHitDF(rating_true, rating_pred, k)
    
    if df_hit.shape[0] == 0:
        return 0.0

    # Calculate Reciprocal Rank
    df_hit_sorted = df_hit.copy()
    df_hit_sorted["rRank"] = (df_hit_sorted.groupby("USER").cumcount() + 1) / df_hit_sorted["rank"]
    df_hit_sorted = df_hit_sorted.groupby("USER").agg({"rRank": "sum"}).reset_index()

    # Calculate Mean Averate Precision
    df_merge = pd.merge(df_hit_sorted, df_hit_count, on="USER")
    return (df_merge["rRank"] / df_merge["actual"]).sum() / n_users

def MeanReciprocalRank(rating_true, rating_pred, k):
    """Calculate Mean Reciprocal Rank at K
    
    Params:
    rating_true (pd.DataFrame): Ground Truth Ratings. There should be no duplicate
    rating_pred (pd.DataFrame): Predicated Ratings.
    k (int): Number of items presented

    Returns:
    float: Mean Reciprocal Rank at K
    """
    df_hit, df_hit_count, n_users = _GetHitDF(rating_true, rating_pred, k)
    
    if df_hit.shape[0] == 0:
        return 0.0

    # Calculate Reciprocal Rank
    df_hit_sorted = df_hit.copy()
    df_hit_sorted["rRank"] = (df_hit_sorted.groupby("USER").cumcount() + 1) / df_hit_sorted["rank"]
    df_hit_sorted = df_hit_sorted.groupby("USER").agg({"rRank": "sum"}).reset_index()

    return df_hit_sorted["rRank"].sum() / n_users
