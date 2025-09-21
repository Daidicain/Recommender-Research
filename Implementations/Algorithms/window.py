import pandas as pd
import networkx as nx
from numba import njit, prange, float64, int64
import tools
import math
import numpy as np
import time

@njit(parallel=False)
def get_windows( items, timestamps, max_window, size):
    # print('hello')
    endloop = 0
    for l in range(size):
        if endloop == 1: break
        r = l
        while timestamps[r] < max_window[l] and r < size-1:

            r += 1

        
        count = r - l + 1
        # print(count, size)

        # window = np.full(count,0, dtype='|S5')
        window = np.empty(count, dtype='U5')
        for i in range(count):
            # print(f'i{i}')
            index = i + l
            window[i] = items[index]

        if r == size-1: endloop = 1
            

            
        # yield 1

        yield window

        # return window
        


def initialize_structures(train, unique_users: np.array, unique_items: np.array, t_window: float):
    '''
    Purpose: This initializes the graph with users
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
    
    # # create graph object
    # G = nx.Graph()

    # # add user nodes
    # G.add_nodes_from( unique_users, bipartite=0)
    # # add item nodes.
    # G.add_nodes_from( unique_items, bipartite=1) 
    
     
    # print('graph created')
    train= train.sort_values('ts')

    # This finds the max window timestamp
    train['max_window_ts'] = train['ts'].apply( lambda t: t + t_window )
    # print(train)

    df = {'user_id': [],'context': [], 'item_id': []}
    context = 0
    
    for i, user in enumerate(unique_users):

        
        

        # user_data = train[train['user_id']=='u196']
        user_data = train[train['user_id']==user]

        # print(user_data)
        # input()

        # print(user_data)
        for group in get_windows(np.ascontiguousarray(user_data['item_id'].values, dtype='U5'), np.ascontiguousarray(user_data['ts'].values, dtype=np.int32), np.ascontiguousarray(user_data['max_window_ts'].values, dtype=np.int32), len(user_data)):
            df['user_id'].extend([user]*len(group))
            df['context'].extend([context]*len(group))
            df['item_id'].extend(group)
           

            context += 1

            # print(context, group)
            # input()
        
           

        # print(df) 
        # input()

        # temp = get_windows(user_data['item_id'].to_numpy(), user_data['ts'].to_numpy(), user_data['max_window_ts'].to_numpy(), len(user_data))
        # temp = get_windows(user_data['item_id'].to_numpy() len(user_data))



        # input()
    # convert from dictionary to a dataframe
    df = pd.DataFrame(df, columns=df.keys())

    return df



def recommender_algorithm(df: pd.DataFrame, train:pd.DataFrame, user: str, k: int) -> dict:
    '''
    Purpose: This function returns all similar users and how similar they are
    Parameters: A bipartite graph, the user to compare and all other users
    Return: a sorted dict of similar users and their scores
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    # Get items that belong to user
    user_items = set(train[ train['user_id'] == user ]['item_id'])
    
    # max_context = df[ df['user_id'] == user ]['context'].max()
    # user_items = set(df[ df['context'] == max_context ]['item_id'])
    # print(user_items)
    # input()
    # print(user_items)
    # print(df, user_items)
    # get users that share items
    related_context_table = df[ df['item_id'].isin(user_items) & df['user_id'] != user ]
    related_context = related_context_table['context'].unique()

    # print(related_context_table)

    # get common items
    common_items = related_context_table['item_id'].unique()
    
    # initialize all items to 0
    items_ranked = dict.fromkeys(common_items, 0)


    # number of neighbours with the same items
    contextCounted = {}
    # print(len(related_context))

    # t1 = time.time()
    for context in related_context:
        # t1 = time.time()
        # get neighbours set
        # context_items = set(df[ df['context'] == context ]['item_id'])
        context_items = set(related_context_table[ related_context_table['context'] == context ]['item_id'])
        # print(time.time()-t1)
        # print('user items', user_items)
        # print(f'context{context}')
        # print(context_items)

        # (neighbour ∩ user) / (neighbour U user)
        jaccardCoefficient = (len(user_items.intersection(context_items)) / len(user_items.union(context_items)))
        # print(time.time()-t1)
        # print(jaccardCoefficient)

        contextCounted[context] = jaccardCoefficient
        # print(time.time()-t1)
        # input()


        # loop through neighbours items
        for item in context_items:

            # increment item by rank amount
            items_ranked[item] += contextCounted[context]
        # input()
    # t2 = time.time()
    # print(t2-t1)

    

    
   
    #remove known items
    try: 
        for item in user_items: items_ranked.pop(item)
    except: 
        pass
        # print('unique item')

    
    # sort neighbours by number of items in common with user
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1])}
    # print(items_ranked)
    
    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(items_ranked) == 0:

        recommend.append(items_ranked.popitem()[0])
    # print(time.time()-t2)
    # print(recommend)


    return recommend
