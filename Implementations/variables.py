'''VALIDATION TESTS'''
# VALIDATION_TESTS = True
VALIDATION_TESTS = False

# B_VALUES = [10,100,1000,10000,100000]
# B_VALUES = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
B_VALUES = ["fullset"]
# B_VALUES = ["subset"]
# A_VALUES = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
A_VALUES = [10,100,1000,10000,100000,1000000,10000000,100000000]

'''DATASETS'''
DATASET = 'movielens'
# DATASET = 'netflix'
# DATASET = 'amazon'
# DATASET = 'epinions'
# DATASET = 'myket'

'''ALGORITHMS'''
# SAVE_NAME = 'adamic_adar'
# SAVE_NAME = 'common_neighbours'
SAVE_NAME = 'jaccard_coefficient'
# SAVE_NAME = 'window'
# SAVE_NAME = 'link_score'
# SAVE_NAME = 'preferential_attachment'
# SAVE_NAME = 'temporal'
# SAVE_NAME = 'time_score'

'''VARIABLES'''
A = 1000
B = 100000000

'''SYSTEM'''
<<<<<<< HEAD
CPU_CORES = 40 # number of cores to use
=======
CPU_CORES = 8 # number of cores to use
>>>>>>> bc9ef842851b64487faa58de4d763d525d1c0468
RANDOM_STATE = 45 # keeps tests consistent between runs

