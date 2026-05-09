# Recommender-Research

## Folder/File explanations

    Datasets/                               - Contains all Datasets

    requirements.txt                        - Contains the required python modules

    Implementations/                        - Contains all code for experimentation

        Algorithms/                         - Contains code for each Algorithm
        config.py                           - Contains configurable variables
        debug.py                            - runs program on one process
        test.py                             - code for test
        validation.py                       - code for validation
        tools.py                            - Contains functions used commonly

    results/                                - handles the result outputs and formatting
        csv/                               
            test/                           - raw output from test.py
            validation/                     - raw output from validation.py
            debug/                          - raw output from debug.py
        output/                         
            test/                           - formatted test output
            validation/                     - formatted validation output
            time_results.json               - run times for each algorithm

        config.py                           - Contains configurable variables 
        initialize.py                       - ensures results file structures are ready
        validation.py                       - formats the validation raw outputs into readable format
        create_table.py                     - formats the test raw outputs into readable format

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

In the Implementations/config.py file, the variable T_VALUES is a list containing every window size to be validated. This program will print a final summary. It will also export the results to the file results/csv/validation/Dataset/Algorithm.csv.

*Note the Validation step should only be run on ttcar Algorithm*

    python Implementations/validation.py
      
## 6. Run Test

In the Implementations/config.py file, the variable T should be set the an appropriate window size. This program will print a final summary. It will also export the results to the file results/csv/test/Dataset/Algorithm.csv.

    python Implementations/test.py

## Debug
This is a minimal implementation. If there are issues running test.py and validation.py; this version will run as a single process. It will print a final summary. It will also export the results to the file results/csv/debug/Dataset/Algorithm.csm.

    python Implementations/debug.py


