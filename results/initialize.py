'''
Purpose: This file ensures all results and subdirectories are created for the main program to output results

'''

import os

RESULTS_DIRECTORY = [
    "results/csv/test/amazon/",
    "results/csv/test/movielens/",
    "results/csv/test/netflix/",
    "results/csv/validation/amazon/",
    "results/csv/validation/movielens/",
    "results/csv/validation/netflix/",
    "results/output/test/",
    "results/output/validation/amazon/",
    "results/output/validation/movielens/",
    "results/output/validation/netflix/",
]

for directory_path in RESULTS_DIRECTORY:
    os.makedirs(directory_path, exist_ok=True)
    print(f"{directory_path} ensured to exist")