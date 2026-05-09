import networkx as nx
import math
import tools
import numpy as np

GRAPH = True

def initialize_structures(train, unique_users: np.array, unique_items: np.array, **kwargs):
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
    
    # format edges as tuples
    ratings = list(zip(train.user_id, train.item_id, train.rating))

    # add edges between users and items
    G.add_weighted_edges_from(ratings, 'rating')

    print('edges added')

    return G, None, None

def recommender_algorithm(G: nx.graph, user: str, k: int, **kwargs) -> list:
    '''
    Purpose: This function returns k best recommendations in order of best to worst
    Parameters: A bipartite graph, the user to compare and k number of items to recommend
    Return: a list of best to worst recommendations
    '''
    if k <= 0: raise Exception("Cannot recommend when k <= 0")
    
    # Get items that belong to user
    user_items = tools.extractTuple( G.edges(user) )

    # get users that share items
    related_users = set(tools.extractTuple( G.edges(user_items) ))

    # remove user
    related_users.remove(user)

    # number of neighbours with the same items
    neighboursCounted = {}

    # One line function that returns 1/log(|N(u)|)
    adar_index_func = lambda u: 1 / math.log( len( G.edges(u) ) )

    for neighbour in related_users:

        # get neighbours set
        neighbour_items = set( tools.extractTuple(G.edges(neighbour)) )
        
        # intersection between users
        user_intersection = neighbour_items.intersection(user_items)
    
        # sum over each intersection 
        neighboursCounted[neighbour] = sum( map( adar_index_func, user_intersection ) )

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

    
    # Sort items by key. 
    # This creates consistent ordering where items have same score
    items_ranked = {k: v for k, v in sorted(items_ranked.items())}

    # Sort items by value and drop the zeros. 
    # This orders the items and filters irrelevant items.
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1]) if v != 0}

    # List to recommend
    recommend = list()

    # loop through items until recommend list has k items
    while len(recommend) < k and not len(items_ranked) == 0:
        item = items_ranked.popitem()[0]
        recommend.append(item)

    return recommend