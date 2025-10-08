import pandas as pd
import tools
print("hello world")


'''DATASETS'''
DATASET = 'movielens'
# DATASET = 'amazon'
# DATASET = 'netflix'
# DATASET = 'lastfm'

'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
# SAVE_NAME = 'jaccard_coefficient'
SAVE_NAME = 'window'
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



if SAVE_NAME == 'adamic_adar': from Algorithms.adamic_adar import *
if SAVE_NAME == 'common_neighbours': from Algorithms.common_neighbours import *
if SAVE_NAME == 'jaccard_coefficient': from Algorithms.jaccard_coefficient import *
if SAVE_NAME == 'preferential_attachment': from Algorithms.preferential_attachment import *
if SAVE_NAME == 'time_score': from Algorithms.time_score import *
if SAVE_NAME == 'link_score': from Algorithms.link_score import *
if SAVE_NAME == 'temporal': from Algorithms.temporal import *
if SAVE_NAME == 'window': from Algorithms.window_rating import *
# if SAVE_NAME == 'window': from Algorithms.window import *


if __name__=="__main__":

    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS, GRAPH)

    print('users: ',len(unique_users),'items: ', len(unique_items))    

    # initialize stuctures
    G, current_time, context_df = initialize_structures(train=train, unique_users=unique_users, unique_items=unique_items, t_window=1000000000)
    
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

        # get recommendations
        
        recommendations = recommender_algorithm(G=G, context_df=context_df, train=train, user=user, current_time=current_time, unique_items=unique_items, k=100)  
        predict = set(test[test['user_id'] == user]['item_id'].unique())

        print(recommendations)
        print(predict)
        input()
        
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

