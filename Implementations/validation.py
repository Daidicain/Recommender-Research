import pandas as pd
import time
import tools
import math

import multiprocessing as mp
from functools import partial

from config import *

def percentages(progress, total, position):
    h_position = position % 8
    v_position = math.ceil(CPU_CORES/8) - math.floor(position / 8)

    BLOCK_SIZE = 22
    # ANSI Escape Codes
    LINE_UP = f'\033[{v_position}A'
    LINE_DOWN = f'\x1b[{v_position}B'
    # LINE_CLEAR = '\x1b[2K'
    
    if h_position == 0: 
        LINE_RIGHT = ""
        LINE_LEFT = f'\033[{h_position*BLOCK_SIZE}D'
    else:
        LINE_RIGHT = f'\033[{h_position*BLOCK_SIZE}C'
        LINE_LEFT = f'\033[{h_position*BLOCK_SIZE}D'
    
    percent = 100 * (progress / float(total))
    bar = '#' * int(percent/10) + ' ' * (10 - int(percent/10))
    print(f"{LINE_UP}{LINE_RIGHT}{position:>3}|\033[31m{bar}\033[0m|{percent:>5.1f}%{LINE_LEFT}{LINE_DOWN}", end='\r')


def testUsers( users, G, train, test, validation, current_time, unique_items, context_df, T):
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

    # get current process name
    p = mp.current_process()._identity[0] -1

    for index, user in enumerate(users):

        # update progress
        percentages(index, len(users), p)

        # Get items that belong to user
        user_items = train[train['user_id'] == user]['item_id']

        # pass if user has no items
        if len( user_items ) == 0: continue

        # get recommendations
        recommendations = recommender_algorithm(G=G, context_df=context_df, train=train, user=user, current_time=current_time, unique_items=unique_items, B=B, t_window=T, k=100)   
        
        # get values to predict
        predict = set(validation[validation['user_id'] == user]['item_id'].unique())
        
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
    
    # finalize progress bar
    percentages(1, 1, p)
        
    return df_accuracy


def main(T, B):
    '''
    Purpose: intializes data then splits users into groups for each processor
    Parameters: 
    Results: 
    '''
    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS, GRAPH)

    # initialize graph object
    G, current_time, context_df = initialize_structures(train=train, unique_users=unique_users, unique_items=unique_items, t_window=T)

    # This will store testing information
    df_accuracy = {}
    df_accuracy['k'] = []
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []


    # get users
    users = validation['user_id'].unique()

    # split users into groups for each core
    arguments = []
    for i in range(CPU_CORES): arguments.append([]) # create cpu cores amount of lists
    for i in range(len(users)): arguments[i%CPU_CORES].append(users[i]) # split users between created lists

    # Initializes the Progress Bars
    print(f'\n{"-"*79} Process Progress {"-"*79}') # title
    print(f'B={B}, T={T}')

    statement = f'' # initial statment
    for i in range(CPU_CORES):
        if i % 8 == 0: statement += "\n"
        statement += f'{i:>3}|\033[31m          \033[0m|  0.0% '
    print( statement ) # progress bar

    # start timer
    t1 = time.time()

    # create process pool
    with mp.Pool(CPU_CORES) as pool:

        # these variables pass to each instance
        partial_funct = partial(testUsers, G=G, train=train, test=test, current_time=current_time, unique_items=unique_items, validation=validation, context_df=context_df, T=T)
        
        # get result for each group of arguments "users"
        for result in pool.map(partial_funct, arguments):

            # record results
            df_accuracy['k'].extend(result['k'])
            df_accuracy['user_id'].extend(result['user_id'])
            df_accuracy['precision@k'].extend(result['precision@k'])
            df_accuracy['recall@k'].extend(result['recall@k'])
            df_accuracy['maPrecision'].extend(result['maPrecision'])

    # print time elapsed
    print(f'time elapsed:{time.time()-t1:2.2f}s')


    # convert from dictionary to a dataframe
    df_accuracy = pd.DataFrame(df_accuracy, columns=df_accuracy.keys())

    # save results to file
    df_accuracy.to_csv(f'results/csv/validation/{DATASET}/{SAVE_NAME}_B={B}_A={T:.2f}.csv')

    # clear line
    print('\x1b[2K', end='\n')



if __name__=="__main__":
    # loop through validation variables
    
    for T_validation in T_VALUES:
        main(T_validation,SAVE_NAME)

    



