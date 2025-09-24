CONFIG = { 
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
