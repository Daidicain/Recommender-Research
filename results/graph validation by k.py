import pandas as pd
import matplotlib.pyplot as plt
import os

# open csvs
COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']

# the different tests that were run
TESTS = ['precision@k','recall@k','maPrecision']

VALIDATION_VALUES = [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000 ]

ALGORITHM = 'ttcar'

# colours available
COLOURS = [(0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(0.5,0.5,1),(1,0.5,0.5),(0.5,1,0.5)]

# directory of the csv's
directory_list = os.listdir('results/csv/validation/') 

# each dataset tested
for dataset in directory_list:


        # Loop through each test type
        for test in TESTS:
                    
            for validation in VALIDATION_VALUES:
                
                # results path
                algorithm_data = f"results/csv/validation/{dataset}/{ALGORITHM}_B={ALGORITHM}_A={validation}.csv"

                # read results
                algorithm_results = pd.read_csv(algorithm_data, usecols= COLUMNS)

                # get x axis = k
                k = algorithm_results['k'].unique()

                # get averages for each k
                algorithm_results2 = algorithm_results.groupby('k').mean()

                # convert from decimal to percent
                algorithm_results2 = algorithm_results2[['precision@k', 'recall@k', 'maPrecision']] * 100

                    
                # colours to cycle through
                # colour = 0

                # get test
                algorithm_test = algorithm_results2[test]

                # Plotting both the curves simultaneously
                # plt.plot(k, algorithm_test, color=COLOURS[colour], label=ALGORITHM.split('.')[0])
                plt.plot(k, algorithm_test, label=validation)

                # increment colour
                # colour += 1
                        
            try:    
                
                # results path
                algorithm_data = f"results/csv/validation/{dataset}/jaccard_coefficient_B=jaccard_coefficient_A=1.csv"

                # read results
                algorithm_results3 = pd.read_csv(algorithm_data, usecols= COLUMNS)
                # get x axis = k
                # k = algorithm_results3['k'].unique()

                # get averages for each k
                algorithm_results3 = algorithm_results3.groupby('k').mean()
                
                # convert from decimal to percent
                algorithm_results3 = algorithm_results3[['precision@k', 'recall@k', 'maPrecision']] * 100
                
                

                algorithm_test = algorithm_results3[test]
                # print('hi')

                # Plotting both the curves simultaneously
                plt.plot(k, algorithm_test, '*', label='jaccard_coefficient', )

            except Exception as e:
                 print(e)
                 pass
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
