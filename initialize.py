import os

RESULTS_DIRECTORY = [
    "results/csv/test/amazon/",
    "results/csv/test/movielens/",
    "results/csv/test/netflix/",
    "results/csv/validation/amazon/",
    "results/csv/validation/movielens/",
    "results/csv/validation/netflix/",
    "results/csv/validation/output/",
    "results/graphs/test/",
    "results/graphs/validation/",
]

for directory_path in RESULTS_DIRECTORY:
    os.makedirs(directory_path, exist_ok=True)
    print(f"{directory_path} ensured to exist")