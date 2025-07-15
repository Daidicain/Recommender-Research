import pandas as pd
import matplotlib.pyplot as plt
import os

# open csvs
COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

# DATASET = 'movielens'
# DATASET = 'netflix'
DATASET = 'amazon'

# directory of the csv's
directory_list = os.listdir(f'results/csv/validation/{DATASET}/')



def test_Results(test):
    print(test)


    # each dataset tested
    for test_results_file in directory_list:

        # check if folder
        if not 'describe' in test_results_file:

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

            A = test_results_file.split("A=")[1].split('_')[0]

            yield algorithm_results

for test in TESTS:
    pd.concat(test_Results(test), axis=1).to_csv(f'results/output/validation/{DATASET}_validation_{test}.csv')

            
