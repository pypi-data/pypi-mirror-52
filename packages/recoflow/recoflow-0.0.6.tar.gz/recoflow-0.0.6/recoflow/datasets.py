import numpy as np 
import pandas as pd 


def SampleData(users, items, ratings):
    sample_movie_id = [1, 71, 95, 50, 176, 82]
    sample_user_id = [1, 2, 6, 7, 8, 10, 12, 13, 14, 16]
    
    sample_ratings = ratings[ratings.user_id.isin(sample_user_id) & ratings.movie_id.isin(sample_movie_id)]
    sample_items = items[items.movie_id.isin(sample_movie_id)]
    sample_users = users[users.user_id.isin(sample_user_id)]
    
    return sample_users, sample_items, sample_ratings
    