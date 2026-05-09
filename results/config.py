


'''The Dataset'''
DATASET = 'movielens'
# DATASET = 'amazon'
# DATASET = 'epinions'

'''k values to display'''
k_values = [1,5,10,20]


'''the different tests that were run'''
TESTS = ['precision@k','recall@k','maPrecision']

'''column names'''
# COLUMNS = ['k', 'precision@k', 'recall@k', 'maPrecision']
COLUMNS = ['k', 'user_id', 'precision@k', 'recall@k', 'maPrecision']