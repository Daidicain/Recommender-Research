import pandas as pd
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



for test in TESTS:
    df_results = {'B':[]}
    
    print(test)
    for results_file in directory_list:
        A = results_file.split("A=")[1].split('_')[0]
        B = results_file.split("B=")[1].split('.csv')[0].lstrip('0')

        if A not in df_results:
            df_results[A] = []
        if B not in df_results['B']:
            df_results['B'].append(B)

        # directory of dataset
        results_file_path = f'results/csv/validation/{DATASET}/{results_file}'          

        # read results
        algorithm_results = pd.read_csv(results_file_path, usecols= COLUMNS)

        # get averages for each
        algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']].mean()

        # convert from decimal to percent
        algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']] * 100

        algorithm_results = algorithm_results[test]

        df_results[A].append(algorithm_results)

        # print(df_results)
        print(f"a={A}, b={B}")
        print(df_results['B'], df_results[0.1])

    df_results = pd.DataFrame(df_results, columns=df_results.keys())

    df_results.to_csv(f'results/output/validation/{DATASET}/{test}.csv', index=False)
