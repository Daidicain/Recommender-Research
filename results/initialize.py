'''
Purpose: This file ensures all subdirectories of results are created for the main program to output results

'''

import os

# directories to be created
RESULTS_DIRECTORY = [
    "results/csv/test/amazon/",
    "results/csv/test/movielens/",
    "results/csv/test/netflix/",
    "results/csv/test/epinions/",
    "results/csv/validation/amazon/",
    "results/csv/validation/movielens/",
    "results/csv/validation/netflix/",
    "results/output/test/",
    "results/output/validation/amazon/",
    "results/output/validation/movielens/",
    "results/output/validation/netflix/",
    "results/output/validation/epinions/",
]

# loop through each directory given
for directory_path in RESULTS_DIRECTORY:

    # creates directories from a path
    os.makedirs(directory_path, exist_ok=True)

    # confirmation
    print(f"{directory_path} ensured to exist")