import pandas as pd
import tools



'''DATASETS'''
# DATASET = 'movielens'
DATASET = 'amazon'
# DATASET = 'netflix'
# DATASET = 'lastfm'

'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
SAVE_NAME = 'jaccard_coefficient'
# SAVE_NAME = 'window'
# SAVE_NAME = 'link_score'
# SAVE_NAME = 'preferential_attachment'
# SAVE_NAME = 'temporal'
# SAVE_NAME = 'time_score'
# SAVE_NAME = 'ts'

'''Variables'''
RANDOM_STATE = 45
# RANDOM_STATE = 1000

A = 0.5
B1 = 10
B2 = 10



'''load data info'''
from data_info import *

DATAPATH = CONFIG[DATASET]['DATAPATH']
COLUMN_NAMES = CONFIG[DATASET]['COLUMN_NAMES']
DELIMITER = CONFIG[DATASET]['DELIMITER']
SKIPROWS = CONFIG[DATASET]['SKIPROWS']






# from Algorithms.prop_flow import prop_flow, initialize_structures



if SAVE_NAME == 'adamic_adar': import Algorithms.adamic_adar as adamic_adar
if SAVE_NAME == 'common_neighbours': import Algorithms.common_neighbours as common_neighbours
if SAVE_NAME == 'jaccard_coefficient': import Algorithms.jaccard_coefficient as jaccard_coefficient
if SAVE_NAME == 'preferential_attachment': import Algorithms.preferential_attachment as preferential_attachment
if SAVE_NAME == 'time_score': import Algorithms.time_score as time_score
if SAVE_NAME == 'link_score': import Algorithms.link_score as link_score
if SAVE_NAME == 'temporal': import Algorithms.temporal as temporal
if SAVE_NAME == 'window': import Algorithms.window as window


if __name__=="__main__":

    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS)

    print('users: ',len(unique_users),'items: ', len(unique_items))

    G=None
    mostRecentYear = None
    df = None
    
    # initialize graph object
    if SAVE_NAME == 'adamic_adar': G = adamic_adar.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'common_neighbours': G = common_neighbours.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'jaccard_coefficient': G = jaccard_coefficient.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'preferential_attachment': G = preferential_attachment.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'time_score': G, mostRecentYear = time_score.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'link_score': G, mostRecentYear = link_score.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'temporal': G = temporal.initialize_structures(train, unique_users, unique_items, A, B1)
    if SAVE_NAME == 'window': df = window.initialize_structures(train, unique_users, 1000000000 )

    # This will store testing information
    df_accuracy = {}
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []

    # for user in ['u719170']:#test['user_id'].unique():
    for user in test['user_id'].unique():
        print(user)

        # Get items that belong to user
        user_items = train[train['user_id'] == user]['item_id']

        # pass if user has no items
        if len( user_items ) == 0: continue

        if SAVE_NAME == 'adamic_adar': recommendations = adamic_adar.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'common_neighbours': recommendations = common_neighbours.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'jaccard_coefficient': recommendations = jaccard_coefficient.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'preferential_attachment': recommendations = preferential_attachment.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'time_score': recommendations = time_score.recommender_algorithm(train, user, unique_items, mostRecentYear, 0.5, 100)
        if SAVE_NAME == 'link_score': recommendations = link_score.recommender_algorithm(G, train, user, unique_items, mostRecentYear, 0.5, 100)
        if SAVE_NAME == 'temporal': recommendations = temporal.recommender_algorithm(G, train, user, 100)
        if SAVE_NAME == 'window': recommendations = window.recommender_algorithm(df, train, user, 100)
    

        predict = set(test[test['user_id'] == user]['item_id'].unique())
        
        # get test results
        precisionAtK = tools.precisionAtK(set(recommendations),predict)
        recallAtK = tools.recallAtK(set(recommendations),predict)
        meanAPrecision = tools.meanAveragePrecision(set(recommendations),predict)

        # add results of user to dataframe
        df_accuracy["user_id"].append(user)
        df_accuracy["precision@k"].append(precisionAtK)
        df_accuracy['recall@k'].append(recallAtK)
        df_accuracy['maPrecision'].append(meanAPrecision)

        # print(df_accuracy)
        

    # convert from dictionary to a dataframe
    df_accuracy = pd.DataFrame(df_accuracy, columns=df_accuracy.keys())

    # print the results
    print(df_accuracy.describe(include='all'))

    # df_accuracy.to_csv('temp')

