# CSV converter and establishes statistics for each file
# Data from Sep 2012
# Started code in March 2022
# Written by Louise Head

import os
import glob
import numpy as np
import pandas as pd
import csv

class Federation:

	# Federation class:
		# Number of registered players
		# Number of active registered players
		# Number of female registered players
		# Number of active female registered players

		# Average rating of top 10 active players
		# Average rating of all active players
		# ID of top 10 active players
		# ID of top 10 active female players

		# Number of Titled players under each category

	def __init__(self,name):
		self.name = name
		self.time = []

		# Raw numbers
		self.all = []
		self.all_active = []
		self.female = []
		self.female_active = []
		self.all_rated = []
		self.all_active_rated = []

		# Titles
		self.wcm = []
		self.wcm_active = []
		self.wfm = []
		self.wfm_active = []
		self.wim = []
		self.wim_active = []
		self.wgm = []
		self.wgm_active = []
		self.cm = []
		self.cm_active = []
		self.fm = []
		self.fm_active = []
		self.im = []
		self.im_active = []
		self.gm = []
		self.gm_active = []

		# Rating average and standard deviation
		self.rating_all_mean = []
		self.rating_all_std = []
		self.rating_female_mean = []
		self.rating_female_std = []
		self.rating_top10_mean = []
		self.rating_top10_std = []
		self.rating_female_top10_mean = []
		self.rating_female_top10_std = []

		# Rating average and standard deviation for top 5 girls and boys (U20)
		self.rating_boys_top5_mean = []
		self.rating_boys_top5_std = []
		self.rating_girls_top5_mean = []
		self.rating_girls_top5_std = []

		# Game number average and standard deviation for top 5 girls and boys (U20)
		self.games_boys_top5_mean = []
		self.games_boys_top5_std = []
		self.games_girls_top5_mean = []
		self.games_girls_top5_std = []

# Make directory for statistics from each month to go
outputDataDir = '../dataAllYears'
if not os.path.exists(outputDataDir):
	os.makedirs(outputDataDir)
removalDataDir = '../removalAllYears'
if not os.path.exists(removalDataDir):
	os.makedirs(removalDataDir)

# Find paths
pathYM = glob.glob('../20*/*/')

# List of federations that have been added to federation class
federationObjects = []						# list to store federation objects
federationObjectsCheck = []					# list of names of federations stored as objects

# List of months for extracting time
monthList = ['Jan','Feb','March','April','May','June','July','Aug','Sep','Oct','Nov','Dec']

# Loop through all months
for path in pathYM:

	############################################################################
	# Sorting input and output files and their paths

	# Extract the year and month from the path name
	splitYM = path.split('/')
	year = splitYM[1]
	month = splitYM[2]
	time = float(year) + float(monthList.index(month)/12)
	print('extracting : ',month, year)

	# Locate datafiles and set-up output paths
	filepath = glob.glob('../'+year+'/'+month+'/'+'*.txt')[0] # input
	outdatafileName = outputDataDir+'/'+month+year+'Stats'+'.csv' # output
	outremovalfile = removalDataDir+'/'+month+year+'Removal'+'.csv' # output

	# Set up csv writer for storing output data
	statFile = open(outdatafileName,'w')				# statistics
	statWriter = csv.writer(statFile)
	removalFile = open(outremovalfile,'w')				# quantity of data that has been removed from statistics
	removalWriter = csv.writer(removalFile)

	# Output file headers
	statWriter.writerow(['FIDE Statistics : '+month+' '+year])
	statWriter.writerow([])
	removalWriter.writerow(['FIDE Data Removed From Statistics : '+month+' '+year])
	removalWriter.writerow([])

	############################################################################

	# Read in file and set up pandas dataframe
	df = pd.read_fwf(filepath)

	############################################################################
	# Data handling and re-naming

	# Manipulate the column data
	df = df.replace(np.NaN, '-')                # Replace blank columns with '-'
	df.Name = df.Name.str.replace(',', ';')     # Replace commas in name with ';'

	# Identify the name of column with grade in it and re-name to 'Grade'
	columnGradeName = df.columns.values[7]
	if columnGradeName == 'FOA':
		columnGradeName = df.columns.values[8]
	df.rename(columns={'ID Number':'ID','Rk':'RK',columnGradeName:'Grade','SGm':'Games','Gms':'Games','B-day':'Bday'},inplace=True)		# rename column name

	# To keep datasets consistent with FOA column, and inactivity flag
	if 'FOA' in df.columns:
		df.drop(columns=['FOA'],inplace=True)	# Drop the FOA column if it exists
	df.at[df['Flag']=='wi','Flag'] = 'i'		# Make all 'wi' just 'i'
	df.at[df['Flag']=='w','Flag'] = '-'			# Make all 'w' just '-'

	# Make sure all these columns are upper case / capitals
	df['Tit'] = df['Tit'].str.upper()
	df['WTit'] = df['WTit'].str.upper()
	df['OTit'] = df['OTit'].str.upper()
	df['Sex'] = df['Sex'].str.upper()
	df['Fed'] = df['Fed'].str.upper()

	# Data removal
	OriginalNumber = df.shape[0]				# Original number of entries

	# Remove lines with columns that have moved
	removalWriter.writerow(['Columns that moved'])
	df.drop(df.loc[df['Bday'].astype(str).str.contains(' ')].index,inplace=True)
	removalWriter.writerow(['Birthday',OriginalNumber-df.shape[0]])
	df.drop(df.loc[df['K'].astype(str).str.contains(' ')].index,inplace=True)
	removalWriter.writerow(['K',OriginalNumber-df.shape[0]])
	df.drop(df.loc[df['Grade'].astype(str).str.contains(' ')].index,inplace=True)
	removalWriter.writerow(['Grade',OriginalNumber-df.shape[0]])
	removalWriter.writerow([])

	# Remove lines with columns that are the wrong length
	removalWriter.writerow(['Columns with incorrect length'])
	df.drop(df[(df["K"].astype(int)).astype(str).str.len()!=2].index, inplace=True)
	removalWriter.writerow(['K',OriginalNumber-df.shape[0]])
	df.drop(df[(df["Grade"].astype(int)).astype(str).str.len()!=4].index, inplace=True)
	removalWriter.writerow(['Grade',OriginalNumber-df.shape[0]])

	FinalNumber = df.shape[0]
	if OriginalNumber != FinalNumber:
		print("Data removed = ", OriginalNumber-FinalNumber)

	# Check that some columns don't have Federations that overspill
	for fed in df.Fed:
		if len(fed) > 3:
			print('datafile conversion error. column widths incorrect')
			exit()

	# Re-naming the old formats for titles to new format (including M)
	df.at[df['Tit']=='WC','Tit'] = 'WCM'
	df.at[df['Tit']=='WF','Tit'] = 'WFM'
	df.at[df['Tit']=='WM','Tit'] = 'WIM'
	df.at[df['Tit']=='WI','Tit'] = 'WIM'
	df.at[df['Tit']=='WG','Tit'] = 'WGM'

	# Check that titles only include 'CM,FM,IM,GM,WCM,WIM,WFM,WGM'
	titleOpts = ['CM','FM','IM','GM','WCM','WFM','WIM','WGM']
	for tit in df.Tit:
		if tit != '-' and tit not in titleOpts and tit != 'HM' and tit != 'WH':
			print(tit)

	# Check genders
	sexOpts = ['M','F']
	for sex in df.Sex:
		if sex not in sexOpts:
			print('other option than M or F', sex)
			exit()

	# Set numerical columns to integers
	df['Grade'] = df['Grade'].astype(int)
	df['Bday'] = df['Bday'].astype(int)
	df['Games'] = df['Games'].astype(int)

	############################################################################

	# Order columns :
	colOrder = ['ID','Fed','Sex','Tit','WTit','OTit','Grade','Games','Bday','Flag']
	df = df.reindex(columns=colOrder)

	############################################################################
	# Federations

	# List of federations
	federationList = (df['Fed'].unique()).tolist()		# name of federations

	# Loop through federations
	for federation in federationList:

		############################################################################
		# Initialise federation

		# Initialise federation object into their class
		if federation not in federationObjectsCheck:
			federationObjects.append(Federation(federation))
			federationObjectsCheck.append(federation)

		# Find index (location) for federation in federation list
		index = federationObjectsCheck.index(federation)

		# Set-up new dataframe for each federation
		dh = df.loc[df['Fed'] == federation]

		########################################################################
		# Statistics of federation
		federationObjects[index].time.append(time)

		# Raw Numbers [all,active]
		federationObjects[index].all.append(dh.shape[0])
		federationObjects[index].all_active.append(dh.loc[dh['Flag']=='-'].shape[0])
		federationObjects[index].female.append(dh.loc[dh['Sex']=='F'].shape[0])
		federationObjects[index].female_active.append(dh.loc[(dh['Flag']=='-') & (dh['Sex']=='F')].shape[0])

		federationObjects[index].all_rated.append(dh.loc[dh['Grade']!=0].shape[0])
		federationObjects[index].all_active_rated.append(dh.loc[(dh['Flag']=='-') & (dh['Grade']!=0)].shape[0])

		federationObjects[index].wcm.append(dh.loc[(dh['Tit']=='WCM')].shape[0])
		federationObjects[index].wcm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='WCM')].shape[0])
		federationObjects[index].wfm.append(dh.loc[(dh['Tit']=='WFM')].shape[0])
		federationObjects[index].wfm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='WFM')].shape[0])
		federationObjects[index].wim.append(dh.loc[(dh['Tit']=='WIM')].shape[0])
		federationObjects[index].wim_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='WIM')].shape[0])
		federationObjects[index].wgm.append(dh.loc[(dh['Tit']=='WGM')].shape[0])
		federationObjects[index].wgm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='WGM')].shape[0])
		federationObjects[index].cm.append(dh.loc[(dh['Tit']=='CM')].shape[0])
		federationObjects[index].cm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='CM')].shape[0])
		federationObjects[index].fm.append(dh.loc[(dh['Tit']=='FM')].shape[0])
		federationObjects[index].fm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='FM')].shape[0])
		federationObjects[index].im.append(dh.loc[(dh['Tit']=='IM')].shape[0])
		federationObjects[index].im_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='IM')].shape[0])
		federationObjects[index].gm.append(dh.loc[(dh['Tit']=='GM')].shape[0])
		federationObjects[index].gm_active.append(dh.loc[(dh['Flag']=='-') & (dh['Tit']=='GM')].shape[0])

		# Other Numbers (active only)

		# Cut out inactive and those with ratings of 0 and order by rating
		di = dh.loc[(dh['Flag']=='-') & (dh['Grade']!=0)]
		di = di.sort_values(by=['Grade'],ascending=False)

		# List of ID's for top 10 playersååååå
		# L_id_top = (di.head(10)['ID']).tolist()
		# L_id_top_female = (di.loc[di['Sex']=='F'].head(10)['ID']).tolist()

		# Array of grades to analyse
		gradeArray_all = di['Grade'].to_numpy()
		gradeArray_top = di['Grade'].head(10).to_numpy()
		gradeArray_female = (di.loc[di['Sex']=='F']['Grade']).to_numpy()
		gradeArray_top_female = (di.loc[di['Sex']=='F']['Grade']).head(10).to_numpy()

		# Arrays of top 5 under 20 girls and boys
		di = di.loc[(di['Bday'] != 0) & (di['Bday'] >= (int(year)-20))]
		Junior5_male_grades = di.loc[di['Sex']=='M'].head(5)['Grade'].to_numpy()
		Junior5_female_grades = di.loc[di['Sex']=='F'].head(5)['Grade'].to_numpy()
		Junior5_male_games = di.loc[di['Sex']=='M'].head(5)['Games'].to_numpy()
		Junior5_female_games = di.loc[di['Sex']=='F'].head(5)['Games'].to_numpy()

		# Average rating and standard deviation of ratings
		if len(gradeArray_all) > 0:
			federationObjects[index].rating_all_mean.append(np.mean(gradeArray_all))
			federationObjects[index].rating_all_std.append(np.std(gradeArray_all))
		else:
			federationObjects[index].rating_all_mean.append(0.0)
			federationObjects[index].rating_all_std.append(0.0)
		if len(gradeArray_top) > 0:
			federationObjects[index].rating_top10_mean.append(np.mean(gradeArray_top))
			federationObjects[index].rating_top10_std.append(np.std(gradeArray_top))
		else:
			federationObjects[index].rating_top10_mean.append(0.0)
			federationObjects[index].rating_top10_std.append(0.0)
		if len(gradeArray_female) > 0:
			federationObjects[index].rating_female_mean.append(np.mean(gradeArray_female))
			federationObjects[index].rating_female_std.append(np.std(gradeArray_female))
		else:
			federationObjects[index].rating_female_mean.append(0.0)
			federationObjects[index].rating_female_std.append(0.0)
		if len(gradeArray_top_female) > 0:
			federationObjects[index].rating_female_top10_mean.append(np.mean(gradeArray_top_female))
			federationObjects[index].rating_female_top10_std.append(np.std(gradeArray_top_female))
		else:
			federationObjects[index].rating_female_top10_mean.append(0.0)
			federationObjects[index].rating_female_top10_std.append(0.0)

		# Ratings for top 5 male and female juniors
		if len(Junior5_male_grades) > 0:
			federationObjects[index].rating_boys_top5_mean.append(np.mean(Junior5_male_grades))
			federationObjects[index].rating_boys_top5_std.append(np.std(Junior5_male_grades))
		else:
			federationObjects[index].rating_boys_top5_mean.append(0.0)
			federationObjects[index].rating_boys_top5_std.append(0.0)
		if len(Junior5_female_grades) > 0:
			federationObjects[index].rating_girls_top5_mean.append(np.mean(Junior5_female_grades))
			federationObjects[index].rating_girls_top5_std.append(np.std(Junior5_female_grades))
		else:
			federationObjects[index].rating_girls_top5_mean.append(0.0)
			federationObjects[index].rating_girls_top5_std.append(0.0)

		# Average number games per player for top 5 male and female juniors
		if len(Junior5_male_games) > 0:
			federationObjects[index].games_boys_top5_mean.append(np.mean(Junior5_male_games))
			federationObjects[index].games_boys_top5_std.append(np.std(Junior5_male_games/len(Junior5_male_games)))
		else:
			federationObjects[index].games_boys_top5_mean.append(0.0)
			federationObjects[index].games_boys_top5_std.append(0.0)
		if len(Junior5_male_games) > 0:
			federationObjects[index].games_girls_top5_mean.append(np.mean(Junior5_female_games))
			federationObjects[index].games_girls_top5_std.append(np.std(Junior5_female_games/len(Junior5_female_games)))
		else:
			federationObjects[index].games_girls_top5_mean.append(0.0)
			federationObjects[index].games_girls_top5_std.append(0.0)

		########################################################################

	############################################################################
	# Statistics

	# Total and inactive
	statWriter.writerow(['Players',df.shape[0]])
	statWriter.writerow(['Women',df.loc[df['Sex']=='F'].shape[0]])
	statWriter.writerow(['Men',df.loc[df['Sex']=='M'].shape[0]])
	statWriter.writerow(['Inactive',df.loc[df['Flag']=='i'].shape[0]])
	statWriter.writerow(['Inactive (Women)',df.loc[(df['Flag']=='i') & (df['Sex']=='F')].shape[0]])
	statWriter.writerow([])

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

	############################################################################
	# Age Related Statistics

	# Remove birthdays which aren't in usual format
	df.drop(df[(df["Bday"].astype(int)).astype(str).str.len()!=4].index, inplace=True)
	removalWriter.writerow(['Birthday',OriginalNumber-df.shape[0]])
	removalFile.close()

	# Setting up new dataframe and calculating ages
	statWriter.writerow(['Age', 'All', 'Female'])
	dg = df.loc[(df['Bday']!='-')]
	dg['Bday'] = dg['Bday'].astype(int)
	dg = dg.loc[(df['Bday']!=0)]
	dg.Bday = int(year) - dg.Bday

	for i in range(5,100):
		statWriter.writerow([str(i),dg.loc[dg['Bday'].astype(int)==i & (dg['Grade'].astype(int)>1800) & (dg['Flag']=='i') ].shape[0],dg.loc[(dg['Bday'].astype(int)==i) & (dg['Flag']=='i') & (dg['Grade'].astype(int)>1800) & (dg['Sex']=='F')].shape[0]])
	del(dg)

	statFile.close()
