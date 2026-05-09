import pandas as pd
import tools

from config import *


if __name__=="__main__":

    # get initial data
    unique_users, unique_items, test, train, validation = tools.readData(DATAPATH, COLUMN_NAMES, RANDOM_STATE, DELIMITER, SKIPROWS, GRAPH)

    print('users: ',len(unique_users),'items: ', len(unique_items))    

    # initialize stuctures
    G, current_time, context_df = initialize_structures(train=train, unique_users=unique_users, unique_items=unique_items, t_window=T)
    
    # This will store testing information
    df_accuracy = {}
    df_accuracy['k'] = []
    df_accuracy['user_id'] = []
    df_accuracy['precision@k'] = []
    df_accuracy['recall@k'] = []
    df_accuracy['maPrecision'] = []

    # for user in ['219']:#test['user_id'].unique():
    for user in test['user_id'].unique():
        print('user: ', user)

        # Get items that belong to user
        user_items = train[train['user_id'] == user]['item_id']

        # pass if user has no items
        if len( user_items ) == 0: continue

        # get recommendations
        recommendations = recommender_algorithm(G=G, B=B, context_df=context_df, train=train, user=user, current_time=current_time, unique_items=unique_items,t_window=T , k=100)  
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
        

    # convert from dictionary to a dataframe
    df_accuracy = pd.DataFrame(df_accuracy, columns=df_accuracy.keys())

    # print the results
    print(df_accuracy.describe(include='all'))

    df_accuracy.to_csv(f'results/csv/debug/{DATASET}/{SAVE_NAME}_{T}.csv')

