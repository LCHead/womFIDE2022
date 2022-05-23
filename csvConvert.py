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
	type = 3
	#if int(year) <= 2008:
	#	type = 1		# ID name title country grade games flag
	#elif int(year) <= 2012 and month in [Jan,Feb,March,April,May,June,July]:
	#	type = 2		# ????
	#else:
	#	type = 3		# ID name fed sex tit wtit otit (foa) grade games K Bday Flag

	if type == 3:

		# Read in file as dataframe
		df = pd.read_fwf(filepath)

		# Manipulate the column data
		df = df.replace(np.NaN, '-')                # Replace blank columns with '-'
		df.Name = df.Name.str.replace(',', ';')     # Replace commas in name with ';'

		# Identify the name of column with grade in it
		columnGradeName = df.columns.values[7]
		if columnGradeName == 'FOA':
			columnGradeName = df.columns.values[8]

		df.rename(columns={'ID Number':'ID','Rk':'RK',columnGradeName:'Grade','SGm':'Games','B-day':'Bday'},inplace=True)		# rename column name
		#df.drop(columns=['Name','SK','RRtng','RGm','RK','BRtng','BGm','BK'],inplace=True)						# drop columns
		if 'FOA' in df.columns:
			df.drop(columns=['FOA'],inplace=True)	# Drop the FOA column if it exists
		df.Flag[df['Flag']=='wi'] = 'i'				# Make all 'wi' just 'i'
		df.Flag[df['Flag']=='w'] = '-'				# Make all 'w' just '-'

		# Make sure all these columns are upper case / capitals
		df.Tit.str.upper()
		df.WTit.str.upper()
		df.OTit.str.upper()
		df.Sex.str.upper()

		# Remove lines with columns that have moved
		df.drop(df.loc[df['Bday'].astype(str).str.contains(' ')].index,inplace=True)
		df.drop(df.loc[df['K'].astype(str).str.contains(' ')].index,inplace=True)
		df.drop(df.loc[df['Grade'].astype(str).str.contains(' ')].index,inplace=True)

		# Make sure columns are the right length, or delete from data frame
		df.drop(df[(df["K"].astype(int)).astype(str).str.len()!=2].index, inplace=True)
		df.drop(df[(df["Grade"].astype(int)).astype(str).str.len()!=4].index, inplace=True)
		df.drop(df[(df["Bday"].astype(int)).astype(str).str.len()!=4].index, inplace=True)

		# Checks
		# 1) Check that some columns don't have Federations that overspill too much
		for fed in df.Fed:
		    if len(fed) > 3:
		        print('datafile conversion error. column widths incorrect')
		        exit()

		# 2) Check that titles only include 'CM,FM,IM,GM,WCM,WIM,WFM,WGM'
		titleOpts = ['CM','FM','IM','GM','WCM','WFM','WIM','WGM']
		df.Tit[df['Tit']=='WC'] = 'WCM'
		df.Tit[df['Tit']=='WF'] = 'WFM'
		df.Tit[df['Tit']=='WM'] = 'WIM'
		df.Tit[df['Tit']=='WI'] = 'WIM'
		df.Tit[df['Tit']=='WG'] = 'WGM'
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

		# Statistics
		statFile = open(outdatafileName,'w')
		statWriter = csv.writer(statFile)

		arbiterList = ['IA','FA','NA','IO']
		trainerList = ['FT','FST','DI','NI']

		statWriter.writerow(['FIDE Statistics : '+month+' '+year])
		statWriter.writerow([])

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

		for i in range(5,100):
			statWriter.writerow([str(i),dg.loc[dg['Bday'].astype(int)==i & (dg['Grade'].astype(int)>1800) & (dg['Flag']=='i') ].shape[0],dg.loc[(dg['Bday'].astype(int)==i) & (dg['Flag']=='i') & (dg['Grade'].astype(int)>1800) & (dg['Sex']=='F')].shape[0]])
		del(dg)
		# Looping through ages and finding total number and number of females for each age interval
		#for i in range(0,20):
		#	a = 5*i+1
		#	b = 5*(i+1)
		#	statWriter.writerow(['('+str(a)+'-'+str(b)+')',dg.loc[(dg['Bday']>=a) & (dg['Bday']<= b)].shape[0],dg.loc[(dg['Bday']>=a) & (dg['Bday']<=b) & (dg['Sex']=='F')].shape[0]])
		#del(dg)

		statFile.close()




		# Convert to csv
		#df.to_csv(outfileName,index=False)
