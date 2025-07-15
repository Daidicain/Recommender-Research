CONFIG = { 
    'movielens' : {
        'DATAPATH' : "Datasets/movie lens 100k/u.data",
        'COLUMN_NAMES' : ["user_id","item_id","rating","ts"],
        'DELIMITER' : "	",
        'SKIPROWS' : 0
    },
    'amazon' : {
        'DATAPATH' : "Datasets/tgbl-review-v3/amazon_sample2.csv",
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
        'DATAPATH' : "Datasets/netflix/netflix_sample2.csv",
        'COLUMN_NAMES' : ["item_id","user_id","rating","ts"],
        'DELIMITER' : ",",
        'SKIPROWS' : 1
    }


}
