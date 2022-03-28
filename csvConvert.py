import os
import glob
import numpy as np
import pandas as pd

# Find years

# Find months

# Find files

# Loop through files

filepath = '../2022/Feb/players_list_foa.txt'
filename = '../2022/Feb/player_list.csv'

# Read in file as dataframe
df = pd.read_fwf(filepath)

# Manipulate the column data
df = df.replace(np.NaN, '-')                # Replace blank columns with '-'
df.Name = df.Name.str.replace(',', ';')     # Replace commas in name with ';'

# Convert to csv
df.to_csv(filename,index=False)











### Learning pandas ###

#print(df)           # print dataframe
#print(df.shape)     # print number of rows and columns of data
#print(pd.set_option('display.max_columns',85))
#print(df.info())    # parenthesis if its a method
#print(df.head(50))     # opserve top 50 rows
#print(df.tail(50))     # opserve last 50 rows

# df.loc -- row -- works on labels in my index. df.loc[2] finds the index labelled as 2.
# df.iloc -- column -- works on positions in these index.  looking for values within these indices that are at index 2.

# df.iloc[:,4] = 'columns' :  this works for changing columns
# df.loc[4] = 'rows' : this works for changing rows
