import pandas as pd
import networkx as nx
import tools
import math
import numpy as np


def initialize_structures(train, unique_users: np.array, unique_items: np.array, A: float, B: float):
    '''
    Purpose: This initializes the graph with users
    Parameters: The dataset and two np.arrays unique_users and unique_items.
    Return: a fully initiallized nx.graph
    '''
    # create graph object
    G = nx.Graph()

    # add user nodes
    G.add_nodes_from( unique_users, bipartite=0)
    # add item nodes.
    G.add_nodes_from( unique_items, bipartite=1) 
     
    print('graph created')

    # This allows for conversion from seconds to days
    secondsPerDay = 86400
    train['days'] = train['ts'].apply( lambda t: t/secondsPerDay)

    # This is the most recent day. Starting from this day allows for accurate comparison
    mostRecentDay = train['days'].max()
    
    # OUR TEMPORAL FUNCTIONS
    short_temporal_function = lambda t: (1-A) * (math.e ** -(B * (mostRecentDay - t)))
    long_temporal_function = lambda t: A * (1 - (math.e ** -(B * (mostRecentDay - t))))

    # This calculates the edges weight using the formula 1/e^tB
    train['t_weight'] = train['days'].apply( lambda t: short_temporal_function(t) + long_temporal_function(t) )

    # apply the rating to the weight
    train['t_weight'] = train.apply( lambda row: (row['rating'] * row['t_weight']), axis=1 )

    # add connections between users and items
    timeWeightedEdges = list(zip(train.user_id, train.item_id, train.t_weight))
    timeStampEdges = list(zip(train.user_id, train.item_id, train.days))
    ratings = list(zip(train.user_id, train.item_id, train.rating))

    G.add_weighted_edges_from(timeWeightedEdges)
    G.add_weighted_edges_from(timeStampEdges, 'ts')
    G.add_weighted_edges_from(ratings, 'rating')

    return G, None

def _temporalWeight(train:pd.DataFrame, user1: str, user2: str) -> float:
    '''
    Purpose: given two users and their items return their euclidean distance apart
    Parameters: a graph two users and their items
    Return: float of euclidean distance between users
    '''

    # change for common items
    df1 = train[train['user_id']==user1][['item_id', 't_weight']]
    df2 = train[train['user_id']==user2][['item_id', 't_weight']]

    # intersection of items
    df1 = df1[ df1['item_id'].isin(df2['item_id'])]
    df2 = df2[ df2['item_id'].isin(df1['item_id'])]

    df1 = df1.set_index('item_id').transpose()
    df2 = df2.set_index('item_id').transpose()

    df1 = df1.sort_index(axis=1)
    df2 = df2.sort_index(axis=1)

    # items in general
    # df1 = train[train['user_id']==user1][['item_id', 't_weight']].set_index('item_id').transpose()
    # df2 = train[train['user_id']==user2][['item_id', 't_weight']].set_index('item_id').transpose()

    combined_df = pd.concat([df1, df2], ignore_index=True)
    # print(combined_df)
    
    
    combined_df = combined_df.fillna(0)
    # print(math.e ** (-np.linalg.norm(combined_df.iloc[0]-combined_df.iloc[1])))
    return math.e ** (-np.linalg.norm(combined_df.iloc[0] - combined_df.iloc[[1]]))


def recommender_algorithm(G: nx.graph, train:pd.DataFrame, user: str, k: int) -> dict:
    '''
    Purpose: This function returns all similar users and how similar they are
    Parameters: A bipartite graph, the user to compare and all other users
    Return: a sorted dict of similar users and their scores
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    # Get items that belong to user
    user_items = tools.extractTuple( G.edges(user) )

    # get users that share items
    related_users = set(tools.extractTuple( G.edges(user_items) ))

    # number of neighbours with the same items
    neighboursCounted = {}

    # remove user from set
    related_users.remove(user)

    for neighbour in related_users:
    # for neighbour in ['u185001']:
        # print(neighbour, len(related_users))

        # get neighbours set
        neighbour_items = set( tools.extractTuple(G.edges(neighbour)) )

        # (neighbour ∩ user) / (neighbour U user)
        jaccardCoefficient = (len(neighbour_items.intersection(user_items)) / len(neighbour_items.union(user_items))) * _temporalWeight(train, user, neighbour)

        neighboursCounted[neighbour] = jaccardCoefficient

    # get common items
    common_items = set(tools.extractTuple( G.edges(related_users) ))
    

    # initialize all items to 0
    items_ranked = dict.fromkeys(common_items, 0)

    # loop through each neighbour
    for neighbour in related_users:
        
        # get neighbours items
        neighbour_items = set(tools.extractTuple( G.edges(neighbour) ))

        # loop through neighbours items
        for item in neighbour_items:

            # increment item by rank amount
            items_ranked[item] += neighboursCounted[neighbour]
   
    #remove known items
    try: 
        for item in user_items: items_ranked.pop(item)
    except: 
        pass
        # print('unique item')

    
    # sort neighbours by number of items in common with user
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1])}
    
    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(items_ranked) == 0:

        recommend.append(items_ranked.popitem()[0])

    # print(recommend)

    return recommend