import pandas as pd
from numba import njit
import numpy as np
import time

GRAPH = False
       

@njit(parallel=False)
def get_subsets( items: np.ascontiguousarray, timestamps:np.ascontiguousarray, rating:np.ascontiguousarray, t_window: int, size: int, minimum_size: int) -> np.array:
    '''
    Purpose: This is a generator that generates all subsets of size t_window
    Parameters: 
        Items -> Items that belong to user
        Timestamps -> when an item was rated
        t_window -> The acceptable width of a window
        size -> The number of elements in the array
    Return: Iteratively each subset of items t_window apart
    '''
    # This specifies the initial right index of window
    r: int = 0
    l: int = 0

    # This generates all subsets where l > 0
    while l < size:
        r= l 

        # find max r index for window
        while r < (size-1) and (timestamps[r+1] - timestamps[r]) < t_window:
            r += 1

        # get number of items in array
        count: int = r - l + 1

        # skip windows of size 1
        if count == minimum_size: 
            l = r + 1
            continue

        # initialize array of size count
        window: np.array = np.empty(count, dtype=np.int64)
        window_ratings: np.array = np.empty(count, dtype=np.float64)

        # add items to array
        for i in range(count):
            index = i + l # calculate index
            window[i] = items[index] # add item at index to array

        # add timestamps to array
        for i in range(count):
            index = i + l # calculate index
            window_ratings[i] = rating[index] # add item at index to array

        new_window:bool = False

        l = r + 1

        yield window, window_ratings


def initialize_structures(train: np.array, unique_users: np.array, t_window: int, **kwargs) -> pd.DataFrame:
    '''
    Purpose: This initializes a dataframe of context groups
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
 
    train= train.sort_values('ts')

    # initialize dictionary that will become dataframe
    context_df = {'user_id': [],'context': [], 'item_id': [], 'rating': []}

    # start context group at 0
    context = 0
    
    # create all subsets for user
    for user in unique_users:

        # get list of items and timestamps for user
        user_data = train[train['user_id']==user]
        # print(user_data)
        items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)
        timestamps: np.ascontiguousarray = np.ascontiguousarray(user_data['ts'].values, dtype=np.int64)
        ratings: np.ascontiguousarray = np.ascontiguousarray(user_data['rating'].values, dtype=np.float64)
        # print(user)
        # print(*list(get_subsets(items, timestamps, t_window, len(user_data))), sep='\n')
        # input()
        # record all subsets for user
        for subset, subset_rating in get_subsets(items, timestamps, ratings, t_window, len(user_data), 1):
            # print(subset)
            # input()
            
            # get number of items in subset
            size = len(subset)
            
            # record results
            context_df['user_id'].extend([user]*size)
            context_df['context'].extend([context]*size)
            context_df['item_id'].extend(subset)
            context_df['rating'].extend(subset_rating)
           
            # increment context group
            context += 1

    # convert dictionary to dataframe
    context_df = pd.DataFrame(context_df, columns=context_df.keys())

    return None, None, context_df



def recommender_algorithm(context_df: pd.DataFrame, train: pd.DataFrame, user: str, t_window: int, k: int, **kwargs) -> dict:
    '''
    Purpose: This function returns all similar users and how similar they are
    Parameters: A bipartite graph, the user to compare and all other users
    Return: a sorted dict of similar users and their scores
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    user_data = train[train['user_id']==user]
    # print(user_data)
    items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)
    timestamps: np.ascontiguousarray = np.ascontiguousarray(user_data['ts'].values, dtype=np.int64)
    ratings: np.ascontiguousarray = np.ascontiguousarray(user_data['rating'].values, dtype=np.float64)

    # get users that share items
    related_context_table = context_df[ context_df['item_id'].isin(items) & context_df['user_id'] != user ]
    related_context = related_context_table['context'].unique()



    # get common items
    # initialize all items to 0
    common_items = related_context_table['item_id'].unique()
    items_ranked = dict.fromkeys(common_items, 0)


    # number of neighbours with the same items
    contextCounted = {} 

    for subset_items, subset_rating in get_subsets(items, timestamps, ratings, t_window, len(user_data), 1):
        for context, context_table in related_context_table.groupby('context'):
            
            # context_items = set(related_context_table[ related_context_table['context'] == context ]['item_id'])
            # print('table', time.time() - t)
            # t= time.time()
            context_items = context_table['item_id'].to_list()
            # print('table', time.time() - t)

            
            # (neighbour ∩ user) / (neighbour U user)
            common_items = set(subset_items).intersection(context_items)
            unique_items = set(subset_items).union(context_items)
            jaccardCoefficient = (len(common_items) / len(unique_items))

            # rating_difference = 0
            # total_common_items = len(common_items)
            # for item in common_items:
            #     # if item == 50:
            #     #     print(user_rating, context_rating)

            #     user_rating = user_items[user_items['item_id'] == item]['rating'].item() # first rating
            #     context_rating = context_items_table[context_items_table['item_id'] == item]['rating'].item() # second rating
            #     rating_difference += (-0.25 * abs(user_rating - context_rating)  + 1)/total_common_items # linear formula

            # print(rating_difference)
            # input()

            contextCounted[context] = jaccardCoefficient
            

            # loop through neighbours items
            for item in context_items:
                # if item == 50:
                #     print(contextCounted[context])

                # increment item by rank amount
                items_ranked[item] += contextCounted[context]
            
            # print('dict', time.time() - t)
            # input()
    
    # remove known items
    try: 
        for item in items: items_ranked.pop(item)
    except: 
        pass


    
    # sort neighbours by number of items in common with user
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1])}
    
    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(items_ranked) == 0:

        recommend.append(items_ranked.popitem()[0])



    return recommend