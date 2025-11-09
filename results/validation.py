import pandas as pd
import os

# open csvs
COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

# DATASET = 'movielens'
DATASET = 'netflix'
# DATASET = 'amazon'
# DATASET = 'myket'
# DATASET = 'epinions'

# directory of the csv's
directory_list = os.listdir(f'results/csv/validation/{DATASET}/')           

directory_list = sorted(directory_list)

for test in TESTS:
    df_results = {'B':[]}
    
    print(test)
    for results_file in directory_list:
        # print(results_file)
        A = results_file.split("A=")[1].split('.csv')[0].lstrip('0')
        # print(A)
        B = results_file.split("B=")[1].split('_')[0]
        # print(B)
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
    df_results = pd.DataFrame(df_results, columns=df_results.keys())

    print(df_results)


    df_results.to_csv(f'results/output/validation/{DATASET}_{test}.csv', index=False)
