#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import os
import subprocess 

# NOTE: prior to running this script, merge all the training set text files
#		into combined_data.csv and place it in resources/data/

# get a set of all movie-user tuples in the probe dataset
probe_from_file = set()
with open('resources/probe.txt', 'r') as f:
    movie_id = None
    for line in f.readlines():
        if line.endswith(':\n'):
            movie_id = int(line[:-2])
        else:
            probe_from_file.add((int(line[:-1]), movie_id))


# read combinded data - which is all the date, user, movie and rating data
# in one table
df = pd.read_csv('resources/data/combined_data.csv')

# remove date and rename
df = df.rename(columns = {'num': 'movie_id', 'grade': 'rating'}
	).drop('date', axis = 1)[['user_id', 'movie_id', 'rating']]

# boolean mask of which user-movie pair belongs in the probe data
probe_bool_mask = np.array(list(map(lambda x: x in probe_from_file, 
	df.loc[:, ['user_id', 'movie_id']].itertuples(index=False))))


# split to data (training data) and probe
data_df = df.iloc[~probe_bool_mask, :]
probe_df = df.iloc[probe_bool_mask, :]


data_df.to_csv('resources/data/train.csv', index=False)
probe_df.to_csv('resources/data/probe.csv', index=False)


## This part does the sanity check of making sure there's no leakage

# cut the header, keep only user_id and movie_id 
os.system(' cut -f-2 -d, ./resources/data/train.csv | tail -n +2 > ./resources/data/train_pairs.csv')
os.system(' cut -f-2 -d, ./resources/data/probe.csv | tail -n +2 > ./resources/data/probe_pairs.csv')

# print all user-movie pairs that are in both lists (should be none at all)
print(subprocess.check_output(' sort ./resources/data/train_pairs.csv ./resources/data/probe_pairs.csv --parallel 7 | uniq -d'))

os.system(' rm ./resources/data/*_pairs.csv')
