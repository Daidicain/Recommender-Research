import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# path = "Datasets/movielens32M/ratings.csv"
# column_names = ["user_id","item_id","rating","ts"]
# delimiter = ","
# skiprows = 1

# path = "Datasets/movelens1M/ratings.dat"
# column_names = ["user_id","item_id","rating","ts"]
# delimiter = "::"
# skiprows = 0

# path = "Datasets/movielens new 100k/ratings.csv"
# column_names = ["user_id","item_id","rating","ts"]
# delimiter = ","
# skiprows = 1

# path = "Datasets/movielens new 100k/ratings.csv"
# column_names = ["user_id","item_id","rating","ts"]
# delimiter = ","
# skiprows = 1

# path = "Datasets/movielens32M/ratings.csv"
# column_names = ["user_id","item_id","rating","ts"]
# delimiter = ","
# skiprows = 0


# path = "Datasets/netflix/netflix_sample.csv"
# column_names = ["item_id","user_id","rating","ts"]
# delimiter = ","
# skiprows = 1

path = "Datasets/netflix/data_restructured.csv"
column_names = ["item_id","user_id","rating","ts"]
delimiter = ","
skiprows = 0

# path = "Datasets/amazon/amazon_sample.csv"
# column_names = ["ts","user_id","item_id","rating"]
# delimiter = ","
# skiprows = 1


# read data file
df = pd.read_csv(path, delimiter=delimiter, encoding="utf-8", names=column_names, skiprows=skiprows)
# df['ts'] = df['ts'].astype(str)
print(df.dtypes)
print(df['ts'].max())
print(df['ts'].min())

# gets unique items
items = df['item_id'].unique()

# item index
index = 4

# bell_curve = df[df['item_id']==items[index]]['ts']
bell_curve = df[df['item_id']==55]['ts']
# bell_curve = df['ts']

plt.hist(bell_curve, bins=30, density=True, alpha=0.6, color='g')
plt.title(f'Histogram of Item {items[index]}')
# plt.title(f'Netflix Histogram of all reviews')
plt.xticks(rotation=45, ha='right') # Set ticks and labels, rotate for readability
plt.xlabel('ts')
plt.ylabel('Density')
plt.show()