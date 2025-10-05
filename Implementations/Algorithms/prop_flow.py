import networkx as nx
import math
import tools

GRAPH = True

def prop_flow(G: nx.graph, user: str, k: int) -> dict:
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

    # One line function that returns 1/log(|N(u)|)
    adar_index_func = lambda u: 1 / math.log( len( G.edges(u) ) )

    for neighbour in related_users:

        # get neighbours set
        neighbour_items = set( tools.extractTuple(G.edges(neighbour)) )

        # u ∈ (neighbour ∩ user)
        user_intersection = neighbour_items.intersection(user_items)

        # sum over each intersection 
        neighboursCounted[neighbour] = sum( map( adar_index_func, user_intersection ) )


    # sort neighbours by number of items in common with user
    neighboursSorted = {k: v for k, v in sorted(neighboursCounted.items(), key=lambda item: item[1])}

    # recommendation portion

    # Get items that belong to user
    user_items = tools.extractTuple( G.edges(user) )

    # List to recommend
    recommend = list()
    while len(recommend) < k and not len(neighboursSorted) == 0:
        # grab next neighbour
        neighbour = neighboursSorted.popitem()

        # loop through neighbours items and add to recommended
        for item in G.edges(neighbour[0]):

            # if not already known
            if item[1] not in user_items and len(recommend) < k:
                recommend.append(item[1])

    return recommend