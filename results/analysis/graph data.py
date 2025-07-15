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

        # Loop through each test type
        for test in TESTS:

            # colours to cycle through
            colour = 0

            # loop through each algorithm results
            for algorithm in algorithms_list:
                
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
            

            # Naming the x-axis, y-axis and the whole graph
            plt.title(f'{dataset}\n{test}')
            plt.xlabel("k")
            plt.ylabel("Accuracy (%)")
            # plt.title(test)

            # Adding legend, which helps us recognize the curve according to it's color
            plt.legend()

            # save the figure
            plt.savefig(f'results/outputs/test/{dataset}_{test}')

            plt.close()

            # To load the display window
            # plt.show()