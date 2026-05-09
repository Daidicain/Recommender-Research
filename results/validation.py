'''
Purpose: This file compiles validation results into a readable format. 
Parameters: DATASET in the config.py tells program dataset was validated
outputs: results to results/output/validation/dataset/
'''

import pandas as pd
from config import *
import os

# directory of the csv's
directory_list = os.listdir(f'results/csv/validation/{DATASET}/')           
directory_list = sorted(directory_list)

# get scores for precision, recall, mean 
for test in TESTS:
    df_results = {'delta':[]}
    
    # list the test being performed
    print('\n\n', test)

    # loop through all csv's
    for results_file in directory_list:

        # get delta/algorithm from csv name
        delta = results_file.rsplit("_", 1)[1].rsplit('.csv', 1)[0]
        Algorithm = results_file.rsplit('_', 1)[0]
  
        # confirm algorithm recorded
        if Algorithm not in df_results:
            df_results[Algorithm] = []

        # confirm delta value recorded
        if delta not in df_results['delta']:
            df_results['delta'].append(delta)

        # directory of dataset
        results_file_path = f'results/csv/validation/{DATASET}/{results_file}'          

        # read results
        algorithm_results = pd.read_csv(results_file_path, usecols= COLUMNS)

        # get averages for each
        algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']].mean()

        # convert from decimal to percent
        algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']] * 100

        # record test
        algorithm_results = algorithm_results[test]
        df_results[Algorithm].append(algorithm_results)

    
    # convert to dataframe
    df_results = pd.DataFrame(df_results, columns=df_results.keys())

    # print results
    print(df_results)

    # save results to 
    df_results.to_csv(f'results/output/validation/{DATASET}/{test}.csv', index=False)
