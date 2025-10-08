'''VALIDATION TESTS'''
# VALIDATION_TESTS = True
VALIDATION_TESTS = False

# B_VALUES = [10,100,1000,10000,100000]
# B_VALUES = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
B_VALUES = ["subset"]
# A_VALUES = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
T_VALUES = [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000 ]

'''DATASETS'''
DATASET = 'movielens'
# DATASET = 'netflix'
# DATASET = 'amazon'
# DATASET = 'epinions'
# DATASET = 'myket'

'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
# SAVE_NAME = 'jaccard_coefficient'
# SAVE_NAME = 'window'
SAVE_NAME = 'window_rating'
# SAVE_NAME = 'window_subgraph'
# SAVE_NAME = 'link_score'
# SAVE_NAME = 'preferential_attachment'
# SAVE_NAME = 'temporal'
# SAVE_NAME = 'time_score'

'''VARIABLES'''
A = 1000000000
B = 1000000000
T = 1000

'''SYSTEM'''
CPU_CORES = 12 # number of cores to use
RANDOM_STATE = 45 # keeps tests consistent between runs


'''load data info'''
DATA = { 
    'movielens' : {
        'DATAPATH' : "Datasets/movie lens 100k/u.data",
        'COLUMN_NAMES' : ["user_id","item_id","rating","ts"],
        'DELIMITER' : "	",
        'SKIPROWS' : 0
    },
    'amazon' : {
        'DATAPATH' : "Datasets/amazon/amazon_sample.csv",
        'COLUMN_NAMES' : ["ts","user_id","item_id","rating"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    },
    'lastfm' : {
        'DATAPATH' : "Datasets/last fm/Last.fm_data.csv",
        'COLUMN_NAMES' : ["","user_id","Artist","item_id","Album","ts","Time"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    },
    'netflix' : {
        'DATAPATH' : "Datasets/netflix/netflix_sample.csv",
        'COLUMN_NAMES' : ["item_id","user_id","rating","ts"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    },
    'epinions' : {
        'DATAPATH' : "Datasets/epinions/epinions_sample.csv",
        'COLUMN_NAMES' : ["item_id","user_id","rating", "status", "ts", "modified", "type", "vertical_id"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    }
    ,
    'steam' : {
        'DATAPATH' : "Datasets/steam/epinions_sample.csv",
        'COLUMN_NAMES' : ["user_id", "item_id", "behaviour", "hoursplayed", "ts", "modified", "type", "vertical_id"],
        'DELIMITER' : ",",
        'SKIPROWS' : 0
    },    
    'myket' : {
        'DATAPATH' : "Datasets/myket/myket_sample.csv",
        'COLUMN_NAMES' : ["ts","user_id" ,"item_id" ,"rating"],
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
if SAVE_NAME == 'link_score': from Algorithms.link_score import *
if SAVE_NAME == 'temporal': from Algorithms.temporal import *
if SAVE_NAME == 'window_rating': from Algorithms.window_rating import *
if SAVE_NAME == 'window_subgraph': from Algorithms.window_subgraph import *
if SAVE_NAME == 'window': from Algorithms.window import *


