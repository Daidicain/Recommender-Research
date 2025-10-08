import networkx as nx
from numba import njit, prange, float64, int64
import tools
import numpy as np
import pandas as pd

GRAPH = True

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

    # create graph object
    G = nx.Graph()

    # add user nodes
    G.add_nodes_from( unique_users, bipartite=0)
    # add item nodes.
    G.add_nodes_from( unique_items, bipartite=1) 
     
    print('graph created')
    
    # format edges as tuples
    ratings = list(zip(train.user_id, train.item_id, train.rating))

    # add edges between users and items
    G.add_weighted_edges_from(ratings, 'rating')

    print('edges added')

    return G, train['years'].max()

@njit(parallel=False, locals={
    'latest_time': int64,
    'oldest_time': int64,
    'recency': int64,
    'time_span': int64,
    'harmonic_mean': float64,
    'score': float64,
    'value': float64
})
def link_score_helper(ratings, time_stamps, current_time, length, B):
    ratings = np.asarray(ratings, dtype=np.float64)
    assert ratings.ndim == 2

    all_links = np.empty(length, dtype=np.float64)

    for i in prange(length):
        harmonic_mean = 0.0
        for j in prange(3):
            value = 1.0 / ratings[i, j]
            harmonic_mean += value
        harmonic_mean = 3.0 / harmonic_mean

        # temporal features
        average_time = np.sum(time_stamps) / length
        latest_time = np.max(time_stamps) 
        # recency = current_time - latest_time 
        time_span = current_time - latest_time + 1

        score = ( harmonic_mean * ( B**(current_time - average_time)) ) / time_span
        all_links[i] = score

    return np.sum(all_links) / (3)

def recommender_algorithm(G: nx.graph, train: pd.DataFrame, user: str, unique_items, current_time: int, B: int, k: int, **kwargs) -> dict:
    '''
    Purpose: This function returns users in order of preferential attachment |Γ1(u)| * |Γ1(p)| 
    Parameters: A bipartite graph, the user to compare and all other users, L max length of path, B a damping factor (0< B <1)
    Return: a sorted dict of similar users and their scores
    '''
    
    # Get items that belong to user
    user_items = tools.extractTuple( G.edges(user) )
    
    train2 = train[['user_id','item_id', 'rating', 'years']]

    # Get items that the user does not have
    potential_items = set(unique_items).difference(user_items)

    temp1 = train2[train2['user_id'] == user]
    temp1 = temp1.add_suffix("_x")
 
    LS = {}
    for item in potential_items:
    # for item in ['i121', 'i245', 'i340', 'i56', 'i117', 'i98', 'i268', 'i174', 'i7', 'i1']:
    # for item in ['i1156']:
        # print(item)
        # Get items that belong to user
        item_users = tools.extractTuple( G.edges(item) )

        temp2 = train2[train2['item_id']==item].add_suffix("_z")
 
        

        temp3 = train2[(train2['item_id'].isin(user_items)) | (train['user_id'].isin(item_users))].add_suffix("_y")
 
        result = pd.DataFrame.merge(temp1,temp3, left_on='item_id_x', right_on='item_id_y', how='inner')
        
        result = pd.DataFrame.merge(result,temp2, left_on='user_id_y', right_on='user_id_z',how='inner')
        
        ratings = np.ascontiguousarray(result[['rating_x', "rating_y", "rating_z"]].values, dtype=np.int64)
        time_stamps = np.array(result[['years_x', "years_y", "years_z"]].values, dtype=np.int64) 
        

        LS[item] = link_score_helper(ratings,time_stamps, current_time, len(ratings), B)

    # sort neighbours by number of items in common with user
    itemsSorted = {k: v for k, v in sorted(LS.items(), key=lambda item: item[1])}

    recommendations = list()  
    # itemsSorted = itemsSorted.keys()     
    for _ in range(k): recommendations.append(itemsSorted.popitem()[0])

    return recommendations
