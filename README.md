# Recommender-Research

## Folder/File explanations

    Datasets/ - Contains all Datasets

    Implementations/                        - Contains all code for experimentation
        Algorithms/                         - Contains code for each Algorithm
        data_info.py                        - Contains constants for opening each Dataset
        research.py                         - single processor main file
        research_multicore.py               - multiprocessor main file
        research_multicore Validation.py    - code for validation
        tools.py                            - Contains functions used commonly

    results/                                - Contains collected results from test
        csv/                                - raw output from main
            test/                           - raw output from main in test mode
            validation/                     - raw output from main in validation mode
        output/                             - cleaned and reformated data 
            test/                           - 
            validation/
            time_results.json
        graph data.py                       - takes results from csv/test/ then saves graphs in output/test/
        initialize.py                       - ensures results file structure are ready
        validation.py                       - combines results from validation tests

## Steps to run

All python scripts are designed to be run from the root of this project directory

## 1. Python venv (Recommended)

Setup/Active venv Windows

    python.exe -m venv .venv
    .venv\Scripts\activate

Setup/Active venv Mac/Linux

    python -m venv .venv
    source .venv/bin/activate

## 2. Install dependencies

    python -m pip install --upgrade -r requirements.txt
    

## 3. To initialize results file structure

    python results/initialize.py

## 4. Config File

Open the Implementations/config.py file in a text editor and set the variable cpu_cores to an integer no larger than the number of threads on the cpu.

Then uncomment one Dataset and Algorithm.

## 5. Run Validation

In the  Implementations/config.py file the variable T_VALUES is a list containing every window size to be validated. This program will print a final score along with exporting the results to the file results/csv/Dataset/Algorithm

    python Implementations/research.py

or

    python Implementations/research_multicore.py
      
## 6. Run Test

## Debug

If there are issues running the multicore functions. The debug file will run the test.py program in a single process.

    python Implementations/debug.py


