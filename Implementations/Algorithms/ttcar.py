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
    new_window: bool = False

    # This generates all subsets where l > 0
    for l in range(0, size - 1):

        # find max r index for window
        while r < (size) and timestamps[r] < (timestamps[l] + t_window):
            r += 1
            new_window: bool = True

        # get number of items in array
        count: int = r - l

        # skip windows less than minimum size
        if count < minimum_size: continue
 
        # initialize array of size count
        window: np.array = np.empty(count, dtype=np.int64)
        window_ratings: np.array = np.empty(count, dtype=np.float64)
        window_ts: np.array = np.empty(count, dtype=np.int64)

        if new_window:
            # add items to array
            for i in range(count):
                index = i + l # calculate index
                window[i] = items[index] # add item at index to array

            # add ratings to array
            for i in range(count):
                index = i + l # calculate index
                window_ratings[i] = rating[index] # add item at index to array

            # add timestamps to array
            for i in range(count):
                index = i + l # calculate index
                window_ts[i] = timestamps[index] # add item at index to array

            new_window:bool = False

            yield window, window_ratings, window_ts

def get_clic( user, t_window, train):
    '''
    Purpose: Clusters subsets by overlap
    Paramters: user, windowsize, and data
    Return: set of items clustered
    '''

    # retrieve user data
    user_data = train[train['user_id']==user]
    # print(user_data)
    items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)
    timestamps: np.ascontiguousarray = np.ascontiguousarray(user_data['ts'].values, dtype=np.int64)
    ratings: np.ascontiguousarray = np.ascontiguousarray(user_data['rating'].values, dtype=np.float64)
    
    # generate all subsets of size t_window
    subsets = list( get_subsets(items, timestamps, ratings, t_window, len(user_data), 1) )

    # return empty set if no subsets
    if len(subsets) == 0:
        return set()
    
    # initialize items to bet first subset
    current_clic = set(subsets[0][0])

    # initialize to largest ts in first subset
    largest_ts = subsets[0][2][-1]

    # go through each subset
    for i in range(1, len(subsets)):
        
        if subsets[i][2][0] <= largest_ts:
            
            # update largest ts
            largest_ts = subsets[i][2][-1]

            # add new items
            current_clic = current_clic.union( set(subsets[i][0]) )
        else:

            # if not bigger yield known items
            yield current_clic

            # set new starting values
            current_clic = set(subsets[i][0])
            largest_ts = subsets[i][2][-1]

    # return last clic
    yield current_clic
    

            



def initialize_structures(train: np.array, unique_users: np.array, t_window: int, **kwargs) -> pd.DataFrame:
    '''
    Purpose: This initializes a dataframe of context groups
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
 
    train= train.sort_values('ts')

    # initialize dictionary that will become dataframe
    context_df = {'user_id': [],'context': [], 'item_id': [], 'rating': [], 'ts': []}

    # start context group at 0
    context = 0
    
    # create all subsets for user
    for user in unique_users:

        # get list of items and timestamps for user
        user_data = train[train['user_id']==user]
        items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)
        timestamps: np.ascontiguousarray = np.ascontiguousarray(user_data['ts'].values, dtype=np.int64)
        ratings: np.ascontiguousarray = np.ascontiguousarray(user_data['rating'].values, dtype=np.float64)
        # print(1)
        # for item in get_subsets(items, timestamps, ratings, t_window, len(user_data), 2):
        #     print( item[0])
        # print(2)
        # for item in get_subsets(items, timestamps, ratings, t_window, len(user_data), 1):
        #     print( item[0])

        # print(items)
        # input()
        # print(*list(get_subsets(items, timestamps, t_window, len(user_data))), sep='\n')
        # input()
        # record all subsets for user
        for subset, subset_rating, subset_ts in get_subsets(items, timestamps, ratings, t_window, len(user_data), 2):
            
            # get number of items in subset
            size = len(subset)
            
            # record results
            context_df['user_id'].extend([user]*size)
            context_df['context'].extend([context]*size)
            context_df['item_id'].extend(subset)
            context_df['rating'].extend(subset_rating)
            context_df['ts'].extend(subset_ts)
           
            # increment context group
            context += 1

    # convert dictionary to dataframe
    context_df = pd.DataFrame(context_df, columns=context_df.keys())

    return None, None, context_df



def recommender_algorithm(context_df: pd.DataFrame, train: pd.DataFrame, user: str, t_window:int, k: int, **kwargs) -> dict:
    '''
    Purpose: This function returns all similar users and how similar they are
    Parameters: A bipartite graph, the user to compare and all other users
    Return: a sorted dict of similar users and their scores
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    # Get items that belong to user
    # get list of items and timestamps for user
    user_data = train[train['user_id']==user]
    # print(user_data)
    items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)

    # get users that share items
    related_context_table = context_df[ context_df['item_id'].isin(items) & context_df['user_id'] != user ].sort_values(['context'])
    

    # related_context = related_context_table['context'].unique()


    
    # get common items
    # initialize all items to 0
    common_items = related_context_table['item_id'].unique()
    items_ranked = dict.fromkeys(common_items, 0)

    # number of neighbours with the same items
    contextCounted = {} 

    for user_click in  get_clic(user,t_window, train):
        # print(user_items_set)
        for context, context_table in related_context_table.groupby('context'):
        # for context in related_context:

            # print(f'name {context}')
            # print(context)
            context_items = context_table['item_id'].to_list()
            
            
            
            # context_items_table = related_context_table[ related_context_table['context'] == context ]
            # print(len(related_context_table), len(context_items_table))
            # context_items = context_items_table['item_id']
           
            # (neighbour ∩ user) / (neighbour U user)
            common_items = user_click.intersection(context_items)
            unique_items = user_click.union(context_items)
            jaccardCoefficient = (len(common_items) / len(unique_items))

            contextCounted[context] = jaccardCoefficient
           

            # loop through neighbours items
            for item in context_items:
                # if item == 50:
                #     print(contextCounted[context])

                # increment item by rank amount
                items_ranked[item] += contextCounted[context]
        # print(3,time.time()-t)
            
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

    # print(len(items_ranked.items()))


    return recommend