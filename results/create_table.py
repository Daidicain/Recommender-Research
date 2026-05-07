import pandas as pd

import os

# open csvs
COLUMNS = ['k', 'user_id', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

k_values = [1,5,10,20]

# directory of the csv's
directory_list = os.listdir('results/csv/test/') 



# each dataset tested
for dataset in directory_list:
    # check if folder
    if not '.' in dataset:

        all_data = {'dataset':[], 'algorithm':[], 'k':[], 'Precision@k':[], 'Recall@k':[], 'Mean Average Precision@k':[]}

        # directory of dataset
        algorithms_list = os.listdir(f'results/csv/test/{dataset}/')
        # algorithms_list = ['adamic_adar.csv', 'common_neighbours.csv', 'jaccard_coefficient.csv', 'link_score.csv', 'preferential_attachment.csv', 'temporal.csv', 'time_score.csv']


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
                
                for k in k_values:
                    all_data['dataset'].append(dataset)
                    all_data['algorithm'].append(algorithm.split('.csv')[0])
                    all_data['k'].append(k)

                    all_data['Precision@k'].append(algorithm_results.loc[k]['precision@k'] * 100 )

                    all_data['Recall@k'].append(algorithm_results.loc[k]['recall@k'] * 100 )

                    all_data['Mean Average Precision@k'].append(algorithm_results.loc[k]['maPrecision'] * 100 )

                # print(all)


                

        df = pd.DataFrame(all_data, columns=all_data.keys())
        df.to_csv(f'results/csv/test/{dataset} compiled results.csv', index=False)
        print(df)
            

