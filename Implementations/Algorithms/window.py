import pandas as pd
from numba import njit
import numpy as np
import time

GRAPH = False

# @njit(parallel=False)
# def get_subsets( items: np.ascontiguousarray, timestamps:np.ascontiguousarray, t_window: int, size: int) -> np.array:
#     '''
#     Purpose: This is a generator that generates all subsets of size t_window
#     Parameters: 
#         Items -> Items that belong to user
#         Timestamps -> when an item was rated
#         t_window -> The acceptable width of a window
#         size -> The number of elements in the array
#     Return: Iteratively each subset of items t_window apart
#     '''
#     # This specifies the initial left and right index of window
#     l = 0
#     r = 1

#     # This generates all subsets where l = 0
#     while r < (size) and (timestamps[l] + t_window) > timestamps[r]:
#         r += 1

#         # get number of items in array
#         count = r - l

#         # skip windows of size 1
#         if count == 1: continue
 
#         # initialize array of size count
#         window = np.empty(count, dtype='U5')

#         # add items to array
#         for i in range(count):
#             index = i + l # calculate index
#             window[i] = items[index] # add item at index to array

#         yield window

#     # This specifies the initial right index of window
#     r = 0

#     # This generates all subsets where l > 0
#     for l in range(1, size - 1):

#         # find max r index for window
#         while r < (size) and timestamps[r] < (timestamps[l] + t_window):
#             r += 1

#         # get number of items in array
#         count = r - l

#         # skip windows of size 1
#         if count == 1: continue
 
#         # initialize array of size count
#         window = np.empty(count, dtype='U5')

#         # add items to array
#         for i in range(count):
#             index = i + l # calculate index
#             window[i] = items[index] # add item at index to array

#         yield window
        

@njit(parallel=False)
def get_subsets( items: np.ascontiguousarray, timestamps:np.ascontiguousarray, t_window: int, size: int) -> np.array:
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

        # skip windows of size 1
        if count == 1: continue
 
        # initialize array of size count
        window: np.array = np.empty(count, dtype=np.int64)

        if new_window:
            # add items to array
            for i in range(count):
                index = i + l # calculate index
                window[i] = items[index] # add item at index to array

            new_window:bool = False

            yield window


def initialize_structures(train: np.array, unique_users: np.array, t_window: int, **kwargs) -> pd.DataFrame:
    '''
    Purpose: This initializes a dataframe of context groups
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
 
    train= train.sort_values('ts')

    # initialize dictionary that will become dataframe
    context_df = {'user_id': [],'context': [], 'item_id': []}

    # start context group at 0
    context = 0
    
    # create all subsets for user
    for user in unique_users:

        # get list of items and timestamps for user
        user_data = train[train['user_id']==user]
        # print(user_data)
        items: np.ascontiguousarray = np.ascontiguousarray(user_data['item_id'].values, dtype=np.int64)
        timestamps:np.ascontiguousarray = np.ascontiguousarray(user_data['ts'].values, dtype=np.int64)
        # print(user)
        # print(*list(get_subsets(items, timestamps, t_window, len(user_data))), sep='\n')
        # input()
        # record all subsets for user
        for subset in get_subsets(items, timestamps, t_window, len(user_data)):
            
            # get number of items in subset
            size = len(subset)
            
            # record results
            context_df['user_id'].extend([user]*size)
            context_df['context'].extend([context]*size)
            context_df['item_id'].extend(subset)
           
            # increment context group
            context += 1

    # convert dictionary to dataframe
    context_df = pd.DataFrame(context_df, columns=context_df.keys())

    return None, None, context_df



def recommender_algorithm(context_df: pd.DataFrame, train: pd.DataFrame, user: str, k: int, **kwargs) -> dict:
    '''
    Purpose: This function returns all similar users and how similar they are
    Parameters: A bipartite graph, the user to compare and all other users
    Return: a sorted dict of similar users and their scores
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    # Get items that belong to user
    user_items = set(train[ train['user_id'] == user ]['item_id'])
    
    # max_context = context_df[ context_df['user_id'] == user ]['context'].max()
    # user_items = set(context_df[ context_df['context'] == max_context ]['item_id'])

    # get users that share items
    related_context_table = context_df[ context_df['item_id'].isin(user_items) & context_df['user_id'] != user ]
    related_context = related_context_table['context'].unique()

    # get common items
    common_items = related_context_table['item_id'].unique()
    
    # initialize all items to 0
    items_ranked = dict.fromkeys(common_items, 0)


    # number of neighbours with the same items
    contextCounted = {}


    for context in related_context:
        
        # context_items = set(related_context_table[ related_context_table['context'] == context ]['item_id'])
        # print('table', time.time() - t)
        # t= time.time()
        context_items = related_context_table[ related_context_table['context'] == context ]['item_id'].unique()
        # print('table', time.time() - t)

        
        # (neighbour ∩ user) / (neighbour U user)
        jaccardCoefficient = (len(user_items.intersection(context_items)) / len(user_items.union(context_items)))
        # print('jaccard', time.time() - t)

        contextCounted[context] = jaccardCoefficient

        # loop through neighbours items
        for item in context_items:

            # increment item by rank amount
            items_ranked[item] += contextCounted[context]
        
        # print('dict', time.time() - t)
        # input()

   
    # remove known items
    try: 
        for item in user_items: items_ranked.pop(item)
    except: 
        pass
    
    # sort neighbours by number of items in common with user
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1])}
    
    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(items_ranked) == 0:

        recommend.append(items_ranked.popitem()[0])

    return recommend
