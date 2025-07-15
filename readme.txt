Folder/File explanations

    Datasets/ - Contains all Datasets

    Implementations/ - Contains all code for experimentation
        Algorithms/ - Contains code for each Algorithm
        data_info.py - Contains constants for opening each Dataset
        research.py - single processor main file
        research_multicore.py - multiprocessor main file
        tools.py - Contains functions used commonly

    results/ - Contains collected results from test
        csv/ - main results collected
        graphs/ - visualization of results
        graph data.py - takes results from csv/ and output graphs in graphs/

To install dependencies

    run command: pip install --upgrade -r requirements.txt

To run 

    - open either research.py or research_multicore.py and uncomment only one item from the '''DATASETS''' and '''ALGORITHMS''' respectively.
      This will run the uncommented dataset and algorithm chosen
      
    - to run use command python Implementations/research.py or Implementations/research_multicore.py
      This must be run from the Experiments/ folder or the Dataset will not be found.



