import os
import glob
import numpy as np
import pandas as pd

# Find months

# monthList

# Find files

# Loop through files

# Extract month and year
month = 'Feb'
year = '2022'

# Make a directory for all csv files to go
outputDir = '../playersAllYears'
if not os.path.exists(outputDir):
	os.makedirs(outputDir)

# Find filepaths
filepath = '../'+year+'/'+month+'/'+'players_list_foa.txt'      # input
outfileName = outputDir+'/'+month+year+'.csv'                          # output

# Read in file as dataframe
df = pd.read_fwf(filepath)

# Manipulate the column data
df = df.replace(np.NaN, '-')                # Replace blank columns with '-'
df.Name = df.Name.str.replace(',', ';')     # Replace commas in name with ';'

# Make sure all these columns are upper case / capitals
df.Tit.str.upper()
df.WTit.str.upper()
df.OTit.str.upper()
df.Sex.str.upper()

# Checks
# 1) Check that some columns don't have Federations that overspill too much
for fed in df.Fed:
    if len(fed) > 3:
        print('datafile conversion error. column widths incorrect')
        exit()

# 2) Check that titles only include 'CM,FM,IM,GM,WCM,WIM,WFM,WGM'
titleOpts = ['CM','FM','IM','GM','WCM','WFM','WIM','WGM']
for tit in df.Tit:
    if tit != '-' and tit not in titleOpts:
        print(tit)

# 3) Check genders
sexOpts = ['M','F']
for sex in df.Sex:
    if sex not in sexOpts:
        print(sex)

# NEXT
# STAGE 1
# 1) make sure earlier data types can be converted
# 2) add in all the years data to the months
# 3) convert all to .csv
# 4) all .csv in one directory with naming covention based on month and year

# STAGE 2
# 1) create a directory with processed data in it
# 2) for each task, generate a list of the names and years that satisfy that task
# 3) new directory for each task
# 4) one file (.txt or .csv) that has the figures ready to plot

# Convert to csv
df.to_csv(outfileName,index=False)











### Learning pandas ###

#print(df)           # print dataframe
#print(df.shape)     # print number of rows and columns of data
#print(pd.set_option('display.max_columns',85))
#print(df.info())    # parenthesis if its a method
#print(df.head(50))     # opserve top 50 rows
#print(df.tail(50))     # opserve last 50 rows

# df.Name.str.upper() convert all strings to upper case

# df.loc -- row -- works on labels in my index. df.loc[2] finds the index labelled as 2.
# df.iloc -- column -- works on positions in these index.  looking for values within these indices that are at index 2.

# df.iloc[:,4] = 'columns' :  this works for changing columns
# df.loc[4] = 'rows' : this works for changing rows
