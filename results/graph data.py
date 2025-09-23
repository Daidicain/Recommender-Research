import pandas as pd
import matplotlib.pyplot as plt
import os

# open csvs
COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

# colours available
COLOURS = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)]

# directory of the csv's
directory_list = os.listdir('results/csv/test/') 

# each dataset tested
for dataset in directory_list:

    # check if folder
    if not '.' in dataset:

        # directory of dataset
        algorithms_list = os.listdir(f'results/csv/test/{dataset}/')
        algorithms_list = ['adamic_adar.csv', 'common_neighbours.csv', 'jaccard_coefficient.csv', 'link_score.csv', 'preferential_attachment.csv', 'temporal.csv', 'time_score.csv', 'window.csv', 'window1.csv', 'window2.csv', 'window3.csv']
        algorithms_list = ['adamic_adar.csv', 'common_neighbours.csv', 'jaccard_coefficient.csv', 'time_score.csv', 'window.csv', 'window2.csv', 'windowsmall.csv', 'windowbig.csv']
        print(algorithms_list)
        input()

        # Loop through each test type
        for test in TESTS:

            # colours to cycle through
            colour = 0

            # loop through each algorithm results
            for algorithm in algorithms_list:
                
                try:
                    # check if csv file
                    if '.csv' in algorithm:

                        # results path
                        algorithm_data = f"results/csv/test/{dataset}/{algorithm}"

                        # read results
                        algorithm_results = pd.read_csv(algorithm_data, usecols= COLUMNS)

                        # get x axis = k
                        k = algorithm_results['k'].unique()

                        # get averages for each
                        algorithm_results = algorithm_results.groupby('k')[['precision@k', 'recall@k', 'maPrecision']].mean()

                        # convert from decimal to percent
                        algorithm_results = algorithm_results[['precision@k', 'recall@k', 'maPrecision']] * 100
    
                        # get test
                        algorithm_test = algorithm_results[test]

                        # Plotting both the curves simultaneously
                        plt.plot(k, algorithm_test, color=COLOURS[colour], label=algorithm.split('.')[0])

                        # increment colour
                        colour += 1
                except: pass
            

            # Naming the x-axis, y-axis and the whole graph
            # plt.title(f'{dataset}\n{test}')
            plt.xlabel("k")
            plt.ylabel("Accuracy (%)")
            # plt.title(test)

            # Adding legend, which helps us recognize the curve according to it's color
            plt.legend()

            # save the figure
            plt.savefig(f'results/output/test/{dataset}_{test}')

            plt.close()

            # To load the display window
            # plt.show()