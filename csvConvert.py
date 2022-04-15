# CSV converter and establishes statistics for each file

import os
import glob
import numpy as np
import pandas as pd
import csv

# Make a directory for all csv files to go
outputDir = '../playersAllYears'
if not os.path.exists(outputDir):
	os.makedirs(outputDir)

outputDataDir = '../dataAllYears'
if not os.path.exists(outputDataDir):
	os.makedirs(outputDataDir)

# Find path
pathYM = glob.glob('../20*/*/')

for path in pathYM:
	# Find year and month
	splitYM = path.split('/')
	year = splitYM[1]
	month = splitYM[2]
	print('extracting : ',month, year)

	# Find filepaths
	filepath = glob.glob('../'+year+'/'+month+'/'+'*.txt')[0] # input
	outfileName = outputDir+'/'+month+year+'.csv'             # output
	outdatafileName = outputDataDir+'/'+month+year+'Stats'+'.csv'

	# Specific file type sorting here :
	type = 0
	if int(year) <= 2008:
		type = 1		# ID name title country grade games flag
	elif int(year) <= 2012 and month in [Jan,Feb,March,April,May,June,July]:
		type = 2		# ????
	else:
		type = 3		# ID name fed sex tit wtit otit (foa) grade games K Bday Flag

	if type == 3:

		# Read in file as dataframe
		df = pd.read_fwf(filepath)

		# Manipulate the column data
		df = df.replace(np.NaN, '-')                # Replace blank columns with '-'
		df.Name = df.Name.str.replace(',', ';')     # Replace commas in name with ';'
		df.rename(columns={'ID Number':'ID','Rk':'RK','SRtng':'Grade','SGm':'Games','B-day':'Bday'},inplace=True)		# rename column name
		df.drop(columns=['Name','SK','RRtng','RGm','RK','BRtng','BGm','BK'],inplace=True)						# drop columns
		if 'FOA' in df.columns:
			df.drop(columns=['FOA'],inplace=True)	# Drop the FOA column if it exists
		df.Flag[df['Flag']=='wi'] = 'i'				# Make all 'wi' just 'i'
		df.Flag[df['Flag']=='w'] = '-'				# Make all 'w' just '-'

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

		# Order columns :
		colOrder = ['ID','Fed','Sex','Tit','WTit','OTit','Grade','Games','Bday','Flag']
		df = df.reindex(columns=colOrder)

		# STAGE 2
		# 1) create a directory with processed data in it
		# 2) for each task, generate a list of the names and years that satisfy that task
		# 3) new directory for each task
		# 4) one file (.txt or .csv) that has the figures ready to plot



		# Statistics
		statFile = open(outdatafileName,'w')
		statWriter = csv.writer(statFile)

		arbiterList = ['IA','FA','NA','IO']
		trainerList = ['FT','FST','DI','NI']

		# Total and inactive
		statWriter.writerow(['Players',df.shape[0]])
		statWriter.writerow(['Women',df.loc[df['Sex']=='F'].shape[0]])
		statWriter.writerow(['Men',df.loc[df['Sex']=='M'].shape[0]])
		statWriter.writerow(['Inactive',df.loc[df['Flag']=='i'].shape[0]])
		statWriter.writerow(['Inactive (Women)',df.loc[(df['Flag']=='i') & (df['Sex']=='F')].shape[0]])
		statWriter.writerow([])

		# Arbiters and trainers
		statWriter.writerow(['Arbiters',df.loc[df['OTit'].isin(arbiterList)].shape[0]])
		statWriter.writerow(['Arbiters (Women)',df.loc[(df['OTit'].isin(arbiterList)) & (df['Sex']=='F')].shape[0]])
		statWriter.writerow(['Trainers',df.loc[df['OTit'].isin(trainerList)].shape[0]])
		statWriter.writerow(['Trainers (Women)',df.loc[(df['OTit'].isin(trainerList)) & (df['Sex']=='F')].shape[0]])

		# Setting up new dataframe and casting all ratings as integers
		dg = df.loc[df['Grade']!='-']
		dg['Grade'] = dg['Grade'].astype(int)
		statWriter.writerow([])
		statWriter.writerow(['Players > 1800',dg.loc[(dg['Grade']>1800)].shape[0]])
		statWriter.writerow(['Players > 1800 (Inactive)',dg.loc[(dg['Grade']>1800) & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 1800 (Women)',dg.loc[(dg['Grade']>1800) & (dg['Sex']=='F')].shape[0]])
		statWriter.writerow(['Players > 1800 (Women) (Inactive)',dg.loc[(dg['Grade']>1800) & (dg['Sex']=='F') & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 2100',dg.loc[(dg['Grade']>2100)].shape[0]])
		statWriter.writerow(['Players > 2100 (Inactive)',dg.loc[(dg['Grade']>2100) & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 2100 (Women)',dg.loc[(dg['Grade']>2100) & (dg['Sex']=='F')].shape[0]])
		statWriter.writerow(['Players > 2100 (Women) (Inactive)',dg.loc[(dg['Grade']>2100) & (dg['Sex']=='F') & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow([])
		del(dg)

		# Setting up new dataframe and calculating ages
		statWriter.writerow(['Age', 'All', 'Female'])
		dg = df.loc[(df['Bday']!='-')]
		dg['Bday'] = dg['Bday'].astype(int)
		dg = dg.loc[(df['Bday']!=0)]
		dg.Bday = int(year) - dg.Bday

		# Looping through ages and finding total number and number of females for each age interval
		for i in range(0,19):
			a = 5*i+1
			b = 5*(i+1)
			statWriter.writerow(['('+str(a)+'-'+str(b)+')',dg.loc[(dg['Bday']>=a) & (dg['Bday']<= b)].shape[0],dg.loc[(dg['Bday']>=a) & (dg['Bday']<=b) & (dg['Sex']=='F')].shape[0]])
		del(dg)

		statFile.close()




		# Convert to csv
		df.to_csv(outfileName,index=False)
		# dg.to_csv(outdatafileName,index=False)











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
