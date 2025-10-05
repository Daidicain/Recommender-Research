import networkx as nx
from numba import jit, njit, prange, float64, int64
import tools
import numpy as np
import pandas as pd
import time

GRAPH = False

def initialize_structures(train, unique_users: np.array, unique_items: np.array, **kwargs):
    '''
    Purpose: This initializes the graph with users
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
    # This allows for conversion from seconds to days
    secondsPerDay = 86400
    train['days'] = train['ts'].apply( lambda t: t/secondsPerDay)
    train['datetime'] = pd.to_datetime(train['ts'], unit='s', origin='unix')
    train['years'] = train['datetime'].dt.year

    return None, train['years'].max(), None


@njit(parallel=False, locals={
    'latest_time': int64,
    'oldest_time': int64,
    'recency': int64,
    'time_span': int64,
    'harmonic_mean': float64,
    'score': float64,
    'value': float64
})
def time_score_helper(ratings, time_stamps, current_time, length, B):
    ratings = np.asarray(ratings, dtype=np.float64)
    assert ratings.ndim == 2

    all_links = np.empty(length, dtype=np.float64)

    for i in prange(length):
        harmonic_mean = 0.0
        for j in prange(3):
            value = 1.0 / ratings[i, j]
            harmonic_mean += value
        harmonic_mean = 3.0 / harmonic_mean

        latest_time = np.max(time_stamps[i])
        oldest_time = np.min(time_stamps[i])
        recency = current_time - latest_time
        time_span = latest_time - oldest_time + 1

        score = (harmonic_mean * (B ** recency)) / time_span
        all_links[i] = score

    return np.sum(all_links) 

# @jit(forceobj=True, nogil=True)
def recommender_algorithm(train: pd.DataFrame, user: str, unique_items, current_time: int, B: int, k: int, **kwargs) -> dict:
    '''
    Purpose: This function returns users in order of preferential attachment |Γ1(u)| * |Γ1(p)| 
    Parameters: A bipartite graph, the user to compare and all other users, L max length of path, B a damping factor (0< B <1)
    Return: a sorted dict of similar users and their scores
    '''

    train2 = train[['user_id','item_id', 'rating', 'years']]
    
    # Get user rows and add suff
    temp1 = train2[train2['user_id'] == user].add_suffix("_x")

    # Get items that belong to user
    user_items = temp1['item_id_x'].unique()

    # print(user_items)
    # input()

    # Get items that the user does not have
    potential_items = unique_items[np.isin(unique_items, user_items, invert=True)]
    
    # print(len(potential_items))
    # input()

    TS = np.empty(len(potential_items), dtype=np.float64)
    t =time.time()
    for i in range(len(potential_items)):
        # print(potential_items[i])

        temp2 = train2[train2['item_id']==potential_items[i]].add_suffix("_z")

        # temp3 = train2[(train2['item_id'].isin(user_items)) | (train['user_id'].isin(item_users))].add_suffix("_y")
        temp3 = train2.add_suffix("_y")
 
        result = pd.DataFrame.merge(temp1,temp3, left_on='item_id_x', right_on='item_id_y', how='inner')
        
        result = pd.DataFrame.merge(result,temp2, left_on='user_id_y', right_on='user_id_z',how='inner')
        
        ratings = np.ascontiguousarray(result[['rating_x', "rating_y", "rating_z"]].values, dtype=np.int64)
        time_stamps = np.array(result[['years_x', "years_y", "years_z"]].values, dtype=np.int64) 

        TS[i] = time_score_helper(ratings,time_stamps, current_time, len(ratings), B)
        
    
    # convert two arrays into dataframe
    itemsSorted = pd.DataFrame({"items": potential_items, "score": TS})

    # Sort items by score
    itemsSorted = itemsSorted.sort_values(by='score', ascending=False)

    # print('time taken:',time.time() - t)

    # return top k
    return itemsSorted.head(k)['items']
