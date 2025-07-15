import pandas as pd
import time
import tools
import os
import json

import multiprocessing as mp
from functools import partial

'''TYPE OF TEST'''
# VALIDATION_TESTS = True
VALIDATION_TESTS = False

'''DATASETS'''
# DATASET = 'movielens'
# DATASET = 'netflix'
DATASET = 'amazon'
# DATASET = 'lastfm'

'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
# SAVE_NAME = 'jaccard_coefficient'
# SAVE_NAME = 'link_score'
# SAVE_NAME = 'preferential_attachment'
SAVE_NAME = 'temporal'
# SAVE_NAME = 'time_score'

'''Variables'''
RANDOM_STATE = 45
# RANDOM_STATE = 1000

A = 0.1
B1 = 10
B2 = 10

# number of cores to use
CPU_CORES = 12


'''load data info'''
from data_info import *

DATAPATH = CONFIG[DATASET]['DATAPATH']
COLUMN_NAMES = CONFIG[DATASET]['COLUMN_NAMES']
DELIMITER = CONFIG[DATASET]['DELIMITER']
SKIPROWS = CONFIG[DATASET]['SKIPROWS']


if SAVE_NAME == 'adamic_adar': import Algorithms.adamic_adar as adamic_adar
if SAVE_NAME == 'common_neighbours': import Algorithms.common_neighbours as common_neighbours
if SAVE_NAME == 'jaccard_coefficient': import Algorithms.jaccard_coefficient as jaccard_coefficient
if SAVE_NAME == 'preferential_attachment': import Algorithms.preferential_attachment as preferential_attachment
if SAVE_NAME == 'time_score': import Algorithms.time_score as time_score
if SAVE_NAME == 'link_score': import Algorithms.link_score as link_score
if SAVE_NAME == 'temporal': import Algorithms.temporal as temporal


def testUsers( users, G, train, test, mostRecentDay, unique_items):
    '''
    Purpose: runs the tests for a given set of users returning results
    Parameters: 
    Results: 
    '''


    df_accuracy = {}
    df_accuracy['k'] = []
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []

    total = len(users) - 1

    

    for index, user in enumerate(users):
        print(f'Process ID {os.getpid():>5}:{index:>3}/{total:<3} user:{user}')

        # Get items that belong to user
        user_items = train[train['user_id'] == user]['item_id']

        # pass if user has no items
        if len( user_items ) == 0: continue

        if SAVE_NAME == 'adamic_adar': recommendations = adamic_adar.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'common_neighbours': recommendations = common_neighbours.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'jaccard_coefficient': recommendations = jaccard_coefficient.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'preferential_attachment': recommendations = preferential_attachment.recommender_algorithm(G, user, 100)
        if SAVE_NAME == 'time_score': recommendations = time_score.recommender_algorithm(train, user, unique_items, mostRecentDay, 0.5, 100)
        if SAVE_NAME == 'link_score': recommendations = link_score.recommender_algorithm(G, train, user, unique_items, mostRecentDay, 0.5, 100)
        if SAVE_NAME == 'temporal': recommendations = temporal.recommender_algorithm(G, train, user, 100)

        predict = set(test[test['user_id'] == user]['item_id'].unique())
        
        for k in range(1,101):
            # get test results
            precisionAtK = tools.precisionAtK(set(recommendations[:k]),predict)
            recallAtK = tools.recallAtK(set(recommendations[:k]),predict)
            meanAPrecision = tools.meanAveragePrecision(set(recommendations[:k]),predict)

            # add results of user to dataframe
            df_accuracy["k"].append(k)
            df_accuracy["user_id"].append(user)
            df_accuracy["precision@k"].append(precisionAtK)
            df_accuracy['recall@k'].append(recallAtK)
            df_accuracy['maPrecision'].append(meanAPrecision)
        
    return df_accuracy
  


if __name__=="__main__":
    '''
    Purpose: intializes data then splits users into groups for each processor
    Parameters: 
    Results: 
    '''
    

    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS)

    print('users: ',len(unique_users),'items: ', len(unique_items))

    # initialize graph object
    if SAVE_NAME == 'adamic_adar': G, mostRecentDay = adamic_adar.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'common_neighbours': G, mostRecentDay = common_neighbours.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'jaccard_coefficient': G, mostRecentDay = jaccard_coefficient.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'preferential_attachment': G, mostRecentDay = preferential_attachment.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'time_score': G, mostRecentDay = time_score.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'link_score': G, mostRecentDay = link_score.initialize_structures(train, unique_users, unique_items)
    if SAVE_NAME == 'temporal': G, mostRecentDay = temporal.initialize_structures(train, unique_users, unique_items, A, B1, B2)

    # add time weight edges between users and items
    # mostRecentDay = tools.addTimeWeightEdges(G, train, A, B1, B2)
    # print('edges added')

    # This will store testing information
    df_accuracy = {}
    df_accuracy['k'] = []
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []

    # get unique users
    users = test['user_id'].unique()
    # users = ['u338044']
    # users = ['u915']

    # split users into groups for each core
    arguments = []
    for i in range(CPU_CORES): arguments.append([])
    for i in range(len(users)): arguments[i%CPU_CORES].append(users[i])

    t1 = time.time()
    with mp.Pool(CPU_CORES) as pool:
        partial_funct = partial(testUsers, G=G, train=train, test=test, mostRecentDay=mostRecentDay, unique_items=unique_items)
        for result in pool.map(partial_funct, arguments):
            df_accuracy['k'].extend(result['k'])
            df_accuracy['user_id'].extend(result['user_id'])
            df_accuracy['precision@k'].extend(result['precision@k'])
            df_accuracy['recall@k'].extend(result['recall@k'])
            df_accuracy['maPrecision'].extend(result['maPrecision'])

    # Record time to run
    with open("results/outputs/time_results.json", "r") as file:
        json_file = json.load(file)
       
    if DATASET not in json_file.keys(): json_file[DATASET] = {}
    json_file[DATASET][SAVE_NAME] = time.time()-t1

    with open("results/outputs/time_results.json", "w") as file:
        json.dump(json_file, file, indent=4)

    # print(df_accuracy)
    # convert from dictionary to a dataframe
    df_accuracy = pd.DataFrame(df_accuracy, columns=df_accuracy.keys())

    # print the results
    print(df_accuracy[df_accuracy['k'] == 10].describe(include='all'))

    if VALIDATION_TESTS:
        df_accuracy.to_csv(f'results/csv/validation/{DATASET}/{SAVE_NAME}_A={A:.2f}_B1={B1:.2f}_B2={B2:.2f}.csv')
        
    else:
        df_accuracy.to_csv(f'results/csv/test/{DATASET}/{SAVE_NAME}.csv')



