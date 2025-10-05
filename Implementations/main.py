import pandas as pd
import time
import tools
import json
import numpy as np
import math

import multiprocessing as mp
from functools import partial

from variables import *

'''load data info'''
from data_info import *

DATAPATH = CONFIG[DATASET]['DATAPATH']
COLUMN_NAMES = CONFIG[DATASET]['COLUMN_NAMES']
DELIMITER = CONFIG[DATASET]['DELIMITER']
SKIPROWS = CONFIG[DATASET]['SKIPROWS']

'''import algorithm module'''
if SAVE_NAME == 'adamic_adar': from Algorithms.adamic_adar import *
if SAVE_NAME == 'common_neighbours': from Algorithms.common_neighbours import *
if SAVE_NAME == 'jaccard_coefficient': from Algorithms.jaccard_coefficient import *
if SAVE_NAME == 'preferential_attachment': from Algorithms.preferential_attachment import *
if SAVE_NAME == 'time_score': from Algorithms.time_score import *
if SAVE_NAME == 'link_score': from Algorithms.link_score import *
if SAVE_NAME == 'temporal': from Algorithms.temporal import *
if SAVE_NAME == 'window': from Algorithms.window import *


def progress_bar(progress, total, position):
    # ANSI Escape Codes
    LINE_UP = f'\033[{position}A'
    LINE_DOWN = f'\x1b[{position}B'
    LINE_CLEAR = '\x1b[2K'
    percent = 100 * (progress / float(total))
    # bar = '█' * int(percent) + '-' * (100 - int(percent))
    bar = '#' * int(percent) + '-' * (100 - int(percent))
    print(f"{LINE_UP}{LINE_CLEAR}Process: {CPU_CORES-position:>3} |\033[31m{bar}\033[0m| {percent:.2f}%{LINE_DOWN}", end='\r')

    # if position % 2 == 0:
    #     print(f"{LINE_UP}{LINE_CLEAR}Process: {CPU_CORES-position:>3} |\033[31m{bar}\033[0m| {percent:.2f}%{LINE_DOWN}", end='\r')
    # else:
    #     print(f"{LINE_UP}{LINE_CLEAR}Process: {CPU_CORES-position:>3} |\033[32m{bar}\033[0m| {percent:.2f}%{LINE_DOWN}", end='\r')

def percentages(progress, total, position):
    h_position = position % 8
    v_position = math.ceil(CPU_CORES/8) - math.floor(position / 8)
    # print(position, h_position, v_position)
    BLOCK_SIZE = 22
    # ANSI Escape Codes
    LINE_UP = f'\033[{v_position}A'
    LINE_DOWN = f'\x1b[{v_position}B'
    
    if h_position == 0: 
        LINE_RIGHT = ""
        LINE_LEFT = f'\033[{h_position*BLOCK_SIZE}D'
    else:
        LINE_RIGHT = f'\033[{h_position*BLOCK_SIZE}C'
        LINE_LEFT = f'\033[{h_position*BLOCK_SIZE}D'
    LINE_CLEAR = '\x1b[2K'
    # print(position, v_position , h_position*BLOCK_SIZE)
    percent = 100 * (progress / float(total))
    # bar = '█' * int(percent) + '-' * (100 - int(percent))
    bar = '#' * int(percent/10) + ' ' * (10 - int(percent/10))
    print(f"{LINE_UP}{LINE_RIGHT}{position:>3}|\033[31m{bar}\033[0m|{percent:>5.1f}%{LINE_LEFT}{LINE_DOWN}", end='\r')
    # '{i:^3}\033[31m  0%\033[0m  |  '
    # '{i:>2}          \033[31m  0.0%\033[0m  '

def testUsers( users, G, train, test, validation, current_time, unique_items, context_df):
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

    p = mp.current_process()._identity[0] -1
    # print(p)

    for index, user in enumerate(users):
        # print(f'Process ID {os.getpid():>5}:{index:>3}/{total:<3} user:{user}')
        percentages(index, len(users), p)

        # Get items that belong to user
        user_items = train[train['user_id'] == user]['item_id']

        # pass if user has no items
        if len( user_items ) == 0: continue

        # get recommendations
        recommendations = recommender_algorithm(G=G, context_df=context_df, train=train, user=user, current_time=current_time, unique_items=unique_items, B=B, k=100)   
        

        predict = set(validation[validation['user_id'] == user]['item_id'].unique())
        if VALIDATION_TESTS:
            predict = predict.union(set(test[test['user_id'] == user]['item_id'].unique()))
        
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
    
    percentages(1, 1, p)
        
    return df_accuracy


def main(A, B):
    '''
    Purpose: intializes data then splits users into groups for each processor
    Parameters: 
    Results: 
    '''
    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS, GRAPH)

    # print('users: ',len(unique_users),'items: ', len(unique_items))
    print(f'A={A}, B={B}')

    # initialize graph object
    G, current_time, context_df = initialize_structures(train=train, unique_users=unique_users, unique_items=unique_items, t_window=T)
    
    # add time weight edges between users and items
    # current_time = tools.addTimeWeightEdges(G, train, A, B1, B2)
    # print('edges added')

    # This will store testing information
    df_accuracy = {}
    df_accuracy['k'] = []
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []

    # get unique users

    # set users to either validation or test
    if VALIDATION_TESTS:
        users = validation['user_id'].unique()
    else:
        users = test['user_id'].unique()

    # split users into groups for each core
    arguments = []
    for i in range(CPU_CORES): arguments.append([])
    for i in range(len(users)): arguments[i%CPU_CORES].append(users[i])

    # Initializes the Progress Bars
    print(f'\n{"-"*79} Process Progress {"-"*79}') # title
    # print(f' Process    '*(10)) # title

    statement = f''
    for i in range(CPU_CORES):
        if i % 8 == 0: statement += "\n"
        statement += f'{i:>3}|\033[31m          \033[0m|  0.0% '
    print( statement ) # progress bar


    t1 = time.time()
    with mp.Pool(CPU_CORES) as pool:
        partial_funct = partial(testUsers, G=G, train=train, test=test, current_time=current_time, unique_items=unique_items, validation=validation, context_df=context_df)
        for result in pool.map(partial_funct, arguments):
            df_accuracy['k'].extend(result['k'])
            df_accuracy['user_id'].extend(result['user_id'])
            df_accuracy['precision@k'].extend(result['precision@k'])
            df_accuracy['recall@k'].extend(result['recall@k'])
            df_accuracy['maPrecision'].extend(result['maPrecision'])

    print(f'time elapsed:{time.time()-t1:2.2f}s')

    # Record time to run
    if not VALIDATION_TESTS:
        with open("results/output/time_results.json", "r") as file:
            json_file = json.load(file)
        
        if DATASET not in json_file.keys(): json_file[DATASET] = {}
        json_file[DATASET][SAVE_NAME] = time.time()-t1

        with open("results/output/time_results.json", "w") as file:
            json.dump(json_file, file, indent=4)

    # print(df_accuracy)
    # convert from dictionary to a dataframe
    df_accuracy = pd.DataFrame(df_accuracy, columns=df_accuracy.keys())

    # print the results
    # print(df_accuracy[df_accuracy['k'] == 10].describe(include='all'))

    if VALIDATION_TESTS:
        df_accuracy.to_csv(f'results/csv/validation/{DATASET}/{SAVE_NAME}_A={A:.2f}_B={B:.2f}.csv')
    
    else:
        df_accuracy.to_csv(f'results/csv/test/{DATASET}/{SAVE_NAME}.csv')



if __name__=="__main__":
    if VALIDATION_TESTS:
        for B_validation in B_VALUES:
            for A_validation in A_VALUES:
                main(A_validation,B_validation)
    else:
        main(A,B)
    



