'''
Purpose: This file compiles test results into a readable format. 
Parameters: k_values in the config.py tells program what k values to store
outputs: results to results/output/test/
'''

import pandas as pd
from config import *
import os

# directory of the csv's
directory_list = os.listdir('results/csv/test/') 

# each dataset tested
for dataset in directory_list:
    # check if folder
    if not '.' in dataset:

        all_data = {'dataset':[], 'algorithm':[], 'k':[], 'Precision@k':[], 'Recall@k':[], 'Mean Average Precision@k':[]}

        # directory of dataset
        algorithms_list = os.listdir(f'results/csv/test/{dataset}/')

        # loop through each algorithm results
        for algorithm in algorithms_list:
            
            # check if csv file
            if '.csv' in algorithm and not 'recommendations' in algorithm:

                # results path
                algorithm_data = f"results/csv/test/{dataset}/{algorithm}"

                # read results
                algorithm_results = pd.read_csv(algorithm_data, usecols= COLUMNS)


                # get averages for each
                algorithm_results = algorithm_results.groupby('k')[['precision@k', 'recall@k', 'maPrecision']].mean()
                
                # loop through each k value and store values in lists
                for k in k_values:

                    # store details
                    all_data['dataset'].append(dataset)
                    all_data['algorithm'].append(algorithm.split('.csv')[0])
                    all_data['k'].append(k)
                    
                    # store metrics
                    all_data['Precision@k'].append(algorithm_results.loc[k]['precision@k'] * 100 )
                    all_data['Recall@k'].append(algorithm_results.loc[k]['recall@k'] * 100 )
                    all_data['Mean Average Precision@k'].append(algorithm_results.loc[k]['maPrecision'] * 100 )

        # convert to dataframe
        df = pd.DataFrame(all_data, columns=all_data.keys())

        # save dataframe to csv
        df.to_csv(f'results/output/test/{dataset} compiled results.csv', index=False)

        # print table
        print(df)
            

