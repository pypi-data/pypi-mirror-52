import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors 

def _GetEmbedding(model, name):
    """Function to get embedding for users or items
    
    Params:     
        model (keras model): Keras model which has embedding layer
        names (string): Name of the user or item embedding layer
    
    Returns: 
        embedding (numpy matrix): Embedding layer for user or item
    """
    embedding = model.get_layer(name = name).get_weights()[0]
    return embedding

def UserEmbedding(model, name="UserEmbedding"):
    """Function to get embedding for users
    
    Params:     
        model (keras model): Keras model which has embedding layer
        names (string): Name of the user embedding layer
    
    Returns: 
        embedding (numpy matrix): Embedding layer for users
    """
    return _GetEmbedding(model, name)


def ItemEmbedding(model, name="ItemEmbedding"):
    """Function to get embedding for items
    
    Params:     
        model (keras model): Keras model which has embedding layer
        names (string): Name of the item embedding layer
    
    Returns: 
        embedding (numpy matrix): Embedding layer for items
    """
    return _GetEmbedding(model, name)


def _GetSimilar(embedding, k):
    model_similar_items = NearestNeighbors(n_neighbors=k, algorithm="ball_tree").fit(embedding)
    distances, indices = model_similar_items.kneighbors(embedding)
    
    return distances, indices



def RecommendTopK(model, data, train, k=5):
    
    """
    Params:
        data (pandas.DataFrame): DataFrame of entire rating data
        train (pandas.DataFrame): DataFrame of train rating data
        k (int): number of items for each user

    Returns:
        pd.DataFrame: DataFrame of top k items for each user, sorted by `col_user` and `rank`
    
    """
    
    # Get predictions for all user-item combination
    all_predictions = _GetPredictions(model, data)
    
    # Handle Missing Values
    all_predictions.fillna(0, inplace=True)
    
    # Filter already seen items
    all_predictions_unseen = _FilterBy(all_predictions, train, ["USER", "ITEM"])
    
    recommend_topk_df = _GetTopKItems(all_predictions_unseen, "USER", "RATING_PRED", k=5)
    
    return recommend_topk_df


def GetPredictionsAll(model, data):
    """
    Get predictions for all user-item combinations
    
    Params:
        data (pandas.DataFrame): DataFrame of entire rating data
        model (Keras.model): Trained keras model
        
    Returns:
        pd.DataFrame: DataFrame of rating predictions for each user and each item
        
    """
    # Create the crossjoin for user-item
    user_item = _UserItemCrossJoin(data)
    
    # Score for every user-item combination
    user_item["RATING_PRED"] = model.predict([user_item.USER, user_item.ITEM])
    
    return user_item

