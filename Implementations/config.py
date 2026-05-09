'''
Purpose: This file allows the user to select the algorithm, dataset, and variables used during validation and testing
Last Updated: May 7 2026
'''


'''DATASETS'''
DATASET = 'movielens'
# DATASET = 'amazon'
# DATASET = 'epinions'


'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
# SAVE_NAME = 'jaccard_coefficient'
SAVE_NAME = 'tcar'
# SAVE_NAME = 'preferential_attachment'
# SAVE_NAME = 'time_score'

'''VARIABLES'''
A = 1000000000
B = 0.5
T = 1000

'''VALIDATION TESTS'''
B_VALUES = ["subset"]
T_VALUES = [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000 ]

'''SYSTEM'''
CPU_CORES = 12 # number of cores to use
RANDOM_STATE = 45 # keeps tests consistent between runs


'''load data info'''
DATA = { 
    'movielens' : {
        'DATAPATH' : "Datasets/movielens/ratings.csv",
        'COLUMN_NAMES' : ["user_id","item_id","rating","ts"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    },
    'amazon' : {
        'DATAPATH' : "Datasets/amazon/amazon_sample.csv",
        'COLUMN_NAMES' : ["ts","user_id","item_id","rating"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    },
    'epinions' : {
        'DATAPATH' : "Datasets/epinions/epinions_sample.csv",
        'COLUMN_NAMES' : ["item_id","user_id","rating", "status", "ts", "modified", "type", "vertical_id"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    }
}

DATAPATH = DATA[DATASET]['DATAPATH']
COLUMN_NAMES = DATA[DATASET]['COLUMN_NAMES']
DELIMITER = DATA[DATASET]['DELIMITER']
SKIPROWS = DATA[DATASET]['SKIPROWS']

'''import algorithm module'''
if SAVE_NAME == 'adamic_adar': from Algorithms.adamic_adar import *
if SAVE_NAME == 'common_neighbours': from Algorithms.common_neighbours import *
if SAVE_NAME == 'jaccard_coefficient': from Algorithms.jaccard_coefficient import *
if SAVE_NAME == 'preferential_attachment': from Algorithms.preferential_attachment import *
if SAVE_NAME == 'time_score': from Algorithms.time_score import *
if SAVE_NAME == 'tcar': from Algorithms.tcar import *


