import networkx as nx
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

def recommender_algorithm(G: nx.graph, user: str, k: int, **kwargs) -> dict:
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

    for neighbour in related_users:

        # get neighbours set
        neighbour_items = set( tools.extractTuple(G.edges(neighbour)) )

        # (neighbour ∩ user) / (neighbour U user)
        jaccardCoefficient = len(neighbour_items.intersection(user_items)) / len(neighbour_items.union(user_items))

        neighboursCounted[neighbour] = jaccardCoefficient

    # # remove user from list
    # neighboursCounted.pop(user)

    # # sort neighbours by number of items in common with user
    # neighboursSorted = {k: v for k, v in sorted(neighboursCounted.items(), key=lambda item: item[1])}

    # # recommendation portion

    # # Get items that belong to user
    # user_items = tools.extractTuple( G.edges(user) )
    
    # # List to recommend
    # recommend = list()
    # while len(recommend) < k and not len(neighboursSorted) == 0:
    #     # grab next neighbour
    #     neighbour = neighboursSorted.popitem()

    #     # loop through neighbours items and add to recommended
    #     for item in G.edges(neighbour[0]):

    #         # if not already known
    #         if item[1] not in user_items and len(recommend) < k:
    #             recommend.append(item[1])

    # return recommend

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
    items_ranked = {k: v for k, v in sorted(items_ranked.items())}
    items_ranked = {k: v for k, v in sorted(items_ranked.items(), key=lambda item: item[1]) if v != 0}
    # print(len(items_ranked.keys()))
    # print(items_ranked)
    # input()
    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(items_ranked) == 0:
        item = items_ranked.popitem()[0]
        recommend.append(item)

    return recommend