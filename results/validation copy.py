import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# open csvs
COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

# DATASET = 'movielens'
# DATASET = 'netflix'
DATASET = 'amazon'

# directory of the csv's
directory_list = os.listdir(f'results/csv/validation/{DATASET}/')
# print(directory_list)
# input()

def float_range(start: float, end:float, increment:float):
    '''
    Purpose: generator that increments between start and end value increasing by constant float
    Parameters: 3 floats start, end, and value to increment
    Yield: value incremented
    '''
    index = start
    while index <= end:
        # round else there may be extra zeros followed by random number
        yield round(index,1)

        index += increment

def test_Results(test, A):
    print(test)

    
    # each dataset tested
    for test_results_file in directory_list:

        # check if a in file
        if re.search(f"{A:.2f}", test_results_file):
            print(f"{A:.2f}", test_results_file, re.search(f"{A:.2f}", test_results_file))

            # directory of dataset
            results_file_path = f'results/csv/validation/{DATASET}/{test_results_file}'          

            # read results
            algorithm_results = pd.read_csv(results_file_path, usecols= COLUMNS)

            # get x axis = k
            k = algorithm_results['k'].unique()

            # get averages for each
            algorithm_results = algorithm_results.groupby('k')[['precision@k', 'recall@k', 'maPrecision']].mean()

            # convert from decimal to percent
            algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']] * 100

            algorithm_results = algorithm_results[test]

            B = test_results_file.split("B=")[1].split('.csv')[0]

            yield algorithm_results.rename(f"{B.lstrip('0')}")


for test in TESTS:
    for A in float_range(0,1,0.1):
        new_df = pd.concat(test_Results(test, A), axis=1)
        new_df.to_csv(f'results/output/validation/{DATASET}_validation_{test}_A={A:.2f}.csv')
