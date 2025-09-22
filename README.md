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

## Python venv (Recommended)

setup venv

    python -m venv .venv

To activate venv Windows

    .venv\Scripts\activate

To activate venv Mac/Linux

    source .venv/bin/activate

## Install dependencies

    python -m pip install --upgrade -r requirements.txt
    

## To initialize results file structure

    python Implementations/initialize.py


## To run

Open either research.py or research_multicore.py and uncomment one item from the '''DATASETS''' and '''ALGORITHMS''' respectively. This will run the code for the uncommented dataset and algorithm chosen

    python Implementations/research.py

or

    python Implementations/research_multicore.py
      
*This must be run from the Experiments/ folder or the Dataset will not be found.*


