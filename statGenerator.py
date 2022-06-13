# CSV converter and establishes statistics for each file
# Data from Sep 2012
# Started code in March 2022
# Written by Louise Head

import os
import glob
import numpy as np
import pandas as pd
import csv

import matplotlib.pyplot as plt
import shendrukGroupFormat as ed
from matplotlib.colors import LinearSegmentedColormap as lsc
from pylab import *
plt.style.use('shendrukGroupStyle')

################################################################################
# Subroutines and classes

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

		# Disparity metric
		self.disparity = 0

		# Dummy variable that can be used to sort data
		self.dummy = 0

# Top federations output files and header
def writeHeadersA(openWriter,womenWriter,disparityWriter,open2021Writer,women2021Writer):
	# Writing headers for top federations and rating disparity

	openWriter.writerow(['Top Federations by Average Rating of Top 10 Players'])
	openWriter.writerow([])
	openWriter.writerow(['Rank','Federation','Mean','Standard Deviation'])

	womenWriter.writerow(['Top Federations by Average Rating of Top 10 Female Players'])
	womenWriter.writerow([])
	womenWriter.writerow(['Rank','Federation','Mean','Standard Deviation'])

	disparityWriter.writerow(['Disparity between Average Rating of Top 10 Players (Open - Women)'])
	disparityWriter.writerow([])

	open2021Writer.writerow(['Top Federations by Average Rating of Top 10 Players (Dec 2021)'])
	open2021Writer.writerow([])
	open2021Writer.writerow(['Rank','Federation','Average (Open)','Average (Women)'])

	women2021Writer.writerow(['Top Federations by Average Rating of Top 10 Female Players (Dec 2021)'])
	women2021Writer.writerow([])
	women2021Writer.writerow(['Rank','Federation','Average (Women)','Average (Open)'])

def writeHeadersB(Writer):
	# Writing headers for top federations and rating disparity

	Writer.writerow(['Number of Titled Players'])
	Writer.writerow([])
	Writer.writerow(['Time', 'WCM', 'WCM(a,i)','WFM','WFM(a,i)','WIM',
						'WIM(a,i)','WGM','WGM(a,i)','CM','CM(a,i)','CM(F)',
						'CM(a,i) (F)','FM','FM(a,i)','FM(F)','FM(a,i)(F)',
						'IM','IM(a,i)','IM(F)','IM(a,i)(F)','GM',
						'GM(a,i)','GM(F)','GM(a,i)(F)'])

################################################################################

# Make directory for statistics from each month to go
outputDataDir = '../dataAllYears'
if not os.path.exists(outputDataDir):
	os.makedirs(outputDataDir)
removalDataDir = '../removalAllYears'
if not os.path.exists(removalDataDir):
	os.makedirs(removalDataDir)
titledDir = '../titled'
if not os.path.exists(titledDir):
	os.makedirs(titledDir)
ratingDisDir = '../ratingDistAllYears'
if not os.path.exists(ratingDisDir):
	os.makedirs(ratingDisDir)

# Write header for titled players files
titledFile = open(titledDir+'/'+'Titled'+'.csv','w')
titledWriter = csv.writer(titledFile)
writeHeadersB(titledWriter)

# Find paths
pathYM = glob.glob('../20*/*/')

# List of federations that have been added to federation class
federationObjects = []						# list to store federation objects
federationObjectsCheck = []					# list of names of federations stored as objects

# List of months and years for extracting time
monthList = ['Jan','Feb','March','April','May','June','July','Aug','Sep','Oct','Nov','Dec']
yearList = ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']
intYearList = [2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

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
	outremovalfile = removalDataDir+'/'+month+year+'Removal'+'.csv' # output

	# Set up csv writer for storing output data
	removalFile = open(outremovalfile,'w')				# quantity of data that has been removed from statistics
	removalWriter = csv.writer(removalFile)

	# Output file headers
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
	federationFlag = True
	if federationFlag == True:
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
	# Titled Players

	titledWriter.writerow([time,
		df.loc[df['Tit']=='WCM'].shape[0],df.loc[(df['Tit']=='WCM')&(df['Flag']!='i')].shape[0],
		df.loc[df['Tit']=='WFM'].shape[0],df.loc[(df['Tit']=='WFM')&(df['Flag']!='i')].shape[0],
		df.loc[df['Tit']=='WIM'].shape[0],df.loc[(df['Tit']=='WIM')&(df['Flag']!='i')].shape[0],
		df.loc[df['Tit']=='WGM'].shape[0],df.loc[(df['Tit']=='WGM')&(df['Flag']!='i')].shape[0],
		df.loc[df['Tit']=='CM'].shape[0],df.loc[(df['Tit']=='CM')&(df['Flag']!='i')].shape[0],
		df.loc[(df['Tit']=='CM')&(df['Sex']=='F')].shape[0],df.loc[(df['Tit']=='CM')&(df['Flag']!='i')&(df['Sex']=='F')].shape[0],
		df.loc[df['Tit']=='FM'].shape[0],df.loc[(df['Tit']=='FM')&(df['Flag']!='i')].shape[0],
		df.loc[(df['Tit']=='FM')&(df['Sex']=='F')].shape[0],df.loc[(df['Tit']=='FM')&(df['Flag']!='i')&(df['Sex']=='F')].shape[0],
		df.loc[df['Tit']=='IM'].shape[0],df.loc[(df['Tit']=='IM')&(df['Flag']!='i')].shape[0],
		df.loc[(df['Tit']=='IM')&(df['Sex']=='F')].shape[0],df.loc[(df['Tit']=='IM')&(df['Flag']!='i')&(df['Sex']=='F')].shape[0],
		df.loc[df['Tit']=='GM'].shape[0],df.loc[(df['Tit']=='GM')&(df['Flag']!='i')].shape[0],
		df.loc[(df['Tit']=='GM')&(df['Sex']=='F')].shape[0],df.loc[(df['Tit']=='GM')&(df['Flag']!='i')&(df['Sex']=='F')].shape[0]])

	############################################################################
	# Rating related statistics

	# ratingDisWriter.writerow([ratingbin, prob])

	ratingStatFlag = True
	if ratingStatFlag == True:

		outratingdisfile = ratingDisDir+'/'+month+year+'RatingDist'+'.csv'

		ratingDisFile = open(outratingdisfile,'w')
		ratingDisWriter = csv.writer(ratingDisFile)

		ratingDisWriter.writerow(['Rating Distributions : '+month+' '+year])

		# Setting up histogram bins
		dg = df.loc[(df['Grade']!='-')&(df['Flag']!='i')]
		dg['Grade'] = dg['Grade'].astype(int)
		dg['Bday'] = dg['Bday'].astype(int)
		minRating = 1000
		maxRating = 2900
		nBins = 20
		dx = (maxRating - minRating)/nBins
		bin = np.linspace(minRating+0.5*dx, maxRating-0.5*dx, nBins)
		Male_bin = np.zeros(nBins,dtype=float)
		Female_bin = np.zeros(nBins,dtype=int)

		NumMale = dg.loc[(dg['Sex']=='M')&(dg['Grade']>=minRating)&(dg['Grade']<maxRating)&(int(year) - dg['Bday']>20)].shape[0]
		NumFemale = dg.loc[(dg['Sex']=='F')&(dg['Grade']>=minRating)&(dg['Grade']<maxRating)&(int(year) - dg['Bday']>20)].shape[0]
		ratingDisWriter.writerow(["male = %i, female = %i"%(NumMale,NumFemale)])

		normaliseHistMale = 0
		normaliseHistFemale = 0
		for i in range(nBins):
			binL = minRating+i*dx
			binR = minRating+(i+1)*dx

			Male_bin[i] = dg.loc[(dg['Sex']=='M')&(dg['Grade']>=binL)&(dg['Grade']<binR)&(int(year) - dg['Bday']>20)].shape[0]
			Female_bin[i] = dg.loc[(dg['Sex']=='F')&(dg['Grade']>=binL)&(dg['Grade']<binR)&(int(year) - dg['Bday']>20)].shape[0]

			normaliseHistMale += Male_bin[i]*dx
			normaliseHistFemale += Female_bin[i]*dx
		for i in range(nBins):
			ratingDisWriter.writerow([bin[i],Male_bin[i]/normaliseHistMale,Female_bin[i]/normaliseHistFemale])

		# Bin into n bins

		# Looping through ages and finding total number and number of females for each age interval
		#for i in range(0,20):
		#	a = 5*i+1
		#	b = 5*(i+1)
		#	statWriter.writerow(['('+str(a)+'-'+str(b)+')',dg.loc[(dg['Bday']>=a) & (dg['Bday']<= b)].shape[0],dg.loc[(dg['Bday']>=a) & (dg['Bday']<=b) & (dg['Sex']=='F')].shape[0]])
		#del(dg)

		# Plot here

		# Write to file

		ratingDisFile.close()

	############################################################################
	# Statistics

	globStatFlag = True
	if globStatFlag == True:

		outdatafileName = outputDataDir+'/'+month+year+'Stats'+'.csv' # output
		statFile = open(outdatafileName,'w')				# statistics
		statWriter = csv.writer(statFile)
		statWriter.writerow(['FIDE Statistics : '+month+' '+year])
		statWriter.writerow([])

		# Total and inactive
		statWriter.writerow(['Players',df.loc[df['Flag']!='i'].shape[0]])
		statWriter.writerow(['Women',df.loc[(df['Sex']=='F')&(df['Flag']!='i')].shape[0]])
		statWriter.writerow(['Men',df.loc[(df['Sex']=='M')&(df['Flag']!='i')].shape[0]])
		statWriter.writerow(['Inactive',df.loc[df['Flag']=='i'].shape[0]])
		statWriter.writerow(['Inactive (Women)',df.loc[(df['Flag']=='i') & (df['Sex']=='F')].shape[0]])
		statWriter.writerow([])

		# Setting up new dataframe and casting all ratings as integers
		dg = df.loc[df['Grade']!='-']
		dg['Grade'] = dg['Grade'].astype(int)
		statWriter.writerow([])
		statWriter.writerow(['Players > 1800',dg.loc[(dg['Grade']>1800) & (dg['Flag']!='i')].shape[0]])
		statWriter.writerow(['Players > 1800 (Inactive)',dg.loc[(dg['Grade']>1800) & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 1800 (Women)',dg.loc[(dg['Grade']>1800) & (dg['Sex']=='F') & (dg['Flag']!='i')].shape[0]])
		statWriter.writerow(['Players > 1800 (Women) (Inactive)',dg.loc[(dg['Grade']>1800) & (dg['Sex']=='F') & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 2100',dg.loc[(dg['Grade']>2100) & (dg['Flag']!='i')].shape[0]])
		statWriter.writerow(['Players > 2100 (Inactive)',dg.loc[(dg['Grade']>2100) & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow(['Players > 2100 (Women)',dg.loc[(dg['Grade']>2100) & (dg['Sex']=='F') & (dg['Flag']!='i')].shape[0]])
		statWriter.writerow(['Players > 2100 (Women) (Inactive)',dg.loc[(dg['Grade']>2100) & (dg['Sex']=='F') & (dg['Flag']=='i')].shape[0]])
		statWriter.writerow([])
		del(dg)

		####################################################################
		# Age Related Statistics

		dg = df.loc[(df['Bday']!='-')]

		# Remove birthdays which aren't in usual format
		dg.drop(dg[(dg["Bday"].astype(int)).astype(str).str.len()!=4].index, inplace=True)
		removalWriter.writerow(['Birthday',OriginalNumber-dg.shape[0]])
		removalFile.close()

		# Setting up new dataframe and calculating ages
		statWriter.writerow(['Age', 'Male', 'Female'])
		dg['Bday'] = dg['Bday'].astype(int)
		dg = dg.loc[(df['Bday']!=0)]
		dg.Bday = int(year) - dg.Bday

		# All ratings
		statWriter.writerow(['All'])
		for i in range(5,100):
			statWriter.writerow([str(i),dg.loc[(dg['Bday'].astype(int)==i) &
			(dg['Flag']!='i') & (dg['Sex']=='M') ].shape[0],
			dg.loc[(dg['Bday'].astype(int)==i) & (dg['Flag']!='i') & (dg['Sex']=='F')].shape[0]])

		statWriter.writerow([])
		statWriter.writerow(['1800+'])
		# Rating > 1800
		for i in range(5,100):
			statWriter.writerow([str(i),dg.loc[(dg['Bday'].astype(int)==i) &
			 (dg['Flag']!='i')& (dg['Grade'].astype(int)>1800) & (dg['Sex']=='M')].shape[0],
			 dg.loc[(dg['Bday'].astype(int)==i) & (dg['Flag']!='i') &
			 (dg['Sex']=='F') & (dg['Grade'].astype(int)>1800)].shape[0]])

		statWriter.writerow([])
		statWriter.writerow(['2100+'])
		# Rating > 2100
		for i in range(5,100):
			statWriter.writerow([str(i),dg.loc[(dg['Bday'].astype(int)==i) &
			(dg['Flag']!='i') & (dg['Grade'].astype(int)>2100) & (dg['Sex']=='M')].shape[0],
			dg.loc[(dg['Bday'].astype(int)==i) & (dg['Flag']!='i') &
			 (dg['Sex']=='F') & (dg['Grade'].astype(int)>2100)].shape[0]])

		statWriter.writerow([])
		statWriter.writerow(['inactive'])
		# Inactive
		for i in range(5,100):
			statWriter.writerow([str(i),dg.loc[(dg['Bday'].astype(int)==i) &
			 (dg['Flag']=='i') & (dg['Sex']=='M')].shape[0],dg.loc[(dg['Bday'].astype(int)==i) &
			 (dg['Flag']=='i') & (dg['Sex']=='F')].shape[0]])

		del(dg)
		statFile.close()

titledFile.close()

################################################################################
# Top rated federations
topRatedFederationFlag = False
if topRatedFederationFlag == True:
	topFedsDir = '../topFederations'
	if not os.path.exists(topFedsDir):
		os.makedirs(topFedsDir)

	ratedFedOpen = open(topFedsDir + '/topRated.csv','w')
	rated2021FedOpen = open(topFedsDir + '/top2021Rated.csv','w')
	rated2021FedWomen = open(topFedsDir + '/top2021RatedWomen.csv','w')
	ratedFedWomen = open(topFedsDir + '/topRatedWomen.csv','w')
	disparityMetric = open(topFedsDir + '/disparityMetric.csv','w')

	openWriter = csv.writer(ratedFedOpen)
	open2021Writer = csv.writer(rated2021FedOpen)
	women2021Writer = csv.writer(rated2021FedWomen)
	womenWriter= csv.writer(ratedFedWomen)
	disparityWriter= csv.writer(disparityMetric)

	writeHeadersA(openWriter,womenWriter,disparityWriter,open2021Writer,women2021Writer)


	# Draw a list of federations that have more than 10 active female players for all years
	List2012 = []
	for yrs in range(2012,2022):
		tm = float(yrs + 11/12)

		# Which Federations are in all years?
		for fed_ in federationObjects:

			# if the year is 2012, see if the federation has more than 10 players
			if yrs == 2012:
				if tm in fed_.time:
					tm_index = fed_.time.index(tm)
					if fed_.female_active[tm_index] >= 10:
						List2012.append(fed_)

			# If the year is after 2012, if the fed doesn't have more than 10 players and is in list, then remove.
			else:
				if fed_ in List2012:
					if tm not in fed_.time:
						List2012.remove(fed_)
					else:
						tm_index = fed_.time.index(tm)
						if fed_.female_active[tm_index] < 10:
							List2012.remove(fed_)

	print(len(List2012))
	# Loop through years and write to file
	for yrs in range(2012,2022):
		# Time indicators by year
		tm = float(yrs + 11/12)								# time
		openWriter.writerow(['December '+ str(yrs)])
		womenWriter.writerow(['December '+ str(yrs)])
		disparityWriter.writerow(['December '+ str(yrs)])

		condition_federationObjects = []
		disparity_federationObjects = []

		# Disparity Metric
		disparityMetricList = []

		# Loop through federations,
		for fed_ in federationObjects:
			if tm in fed_.time:
				tm_index = fed_.time.index(tm)
				fed_.dummy = [fed_.rating_top10_mean[tm_index],fed_.rating_top10_std[tm_index],fed_.rating_female_top10_mean[tm_index],fed_.rating_female_top10_std[tm_index]]
				condition_federationObjects.append(fed_)

				# Find averages for rating disparity
				if fed_.rating_top10_mean[tm_index] != 0.0 and fed_.rating_female_top10_mean[tm_index] != 0.0 and fed_.female_active[tm_index] >= 10 and fed_ in List2012:
					disparityMetricList.append(fed_.rating_top10_mean[tm_index]-fed_.rating_female_top10_mean[tm_index])
					disparity_federationObjects.append(fed_)
					# only want to track progress


		# Find Mean and Standard Deviation Disparity Metric
		DisparityMetric = np.array(disparityMetricList)
		DisparityMean = np.mean(disparityMetricList)
		DisparityStd = np.std(disparityMetricList)

		# Write to file
		disparityWriter.writerow(['Mean : ', DisparityMean])
		disparityWriter.writerow(['S.d. : ', DisparityStd])
		disparityWriter.writerow([])
		disparityWriter.writerow(['Rank','Federation','Top10AvrOpen','Top10AvrWomen','Difference','Disparity','Category'])

		############################################################################
		# Standard deviation of disparity metric
		for fed_ in disparity_federationObjects:
			fed_.disparity = (fed_.dummy[0] - fed_.dummy[2]) - DisparityMean

		disparity_federationObjects.sort(key=lambda x: x.disparity)

		number = 1
		for fed_ in disparity_federationObjects:
			if fed_.dummy[0]-fed_.dummy[2] <=300.0:
				catDisparity = 'A'
			elif fed_.dummy[0]-fed_.dummy[2] <=350:
				catDisparity = 'B'
			elif fed_.dummy[0]-fed_.dummy[2] <=400:
				catDisparity = 'C'
			elif fed_.dummy[0]-fed_.dummy[2] <=450:
				catDisparity = 'D'
			elif fed_.dummy[0]-fed_.dummy[2] <=500:
				catDisparity = 'E'
			elif fed_.dummy[0]-fed_.dummy[2] <=550:
				catDisparity = 'F'
			else:
				catDisparity = 'G'

			disparityWriter.writerow([number, fed_.name, fed_.dummy[0],fed_.dummy[2],fed_.dummy[0]-fed_.dummy[2],fed_.disparity, catDisparity])
			number += 1
		disparityWriter.writerow([])

		############################################################################
		# Open

		# Rank by open average rating
		condition_federationObjects.sort(key=lambda x: x.dummy[0],reverse=True)

		# Write to file
		for i in range(10):
			openWriter.writerow([i+1,condition_federationObjects[i].name,condition_federationObjects[i].dummy[0],condition_federationObjects[i].dummy[2]])
		openWriter.writerow([])

		if yrs == 2021:
			number = 1
			for fed_ in condition_federationObjects:
				open2021Writer.writerow([number,fed_.name,fed_.dummy[0],fed_.dummy[2]])
				number += 1


		############################################################################
		# Women

		# Rank by womens average rating
		condition_federationObjects.sort(key=lambda x: x.dummy[2],reverse=True)

		# Write to file
		for i in range(10):
			womenWriter.writerow([i+1,condition_federationObjects[i].name,condition_federationObjects[i].dummy[2],condition_federationObjects[i].dummy[3]])
		womenWriter.writerow([])

		if yrs == 2021:
			number = 1
			for fed_ in condition_federationObjects:
				women2021Writer.writerow([number,fed_.name,fed_.dummy[2],fed_.dummy[1]])
				number += 1

	ratedFedOpen.close()
	ratedFedWomen.close()
	disparityMetric.close()
	rated2021FedOpen.close()
	rated2021FedWomen.close()

############################################################################
# Federation Statistics

juniorFederationFlag = True
if juniorFederationFlag == True:

	federationDataDir = '../federationStatistics'
	if not os.path.exists(federationDataDir):
		os.makedirs(federationDataDir)

	# Overall statistics
	yearList_count_all = [0,0,0,0,0,0,0,0,0,0]
	gameList_count_boys_all = [0,0,0,0,0,0,0,0,0,0]
	gameList_count_girls_all = [0,0,0,0,0,0,0,0,0,0]

	for fed_ in federationObjects:
		fedDirectory = federationDataDir + '/' + fed_.name
		if not os.path.exists(fedDirectory):
			os.makedirs(fedDirectory)

		############################################################################
		# Junior players

		juniorGames = open(fedDirectory + '/junior5games.csv','w')
		juniorGrades = open(fedDirectory + '/junior5grades.csv','w')
		juniorGamesWriter = csv.writer(juniorGames)
		juniorGradesWriter = csv.writer(juniorGrades)
		juniorGamesWriter.writerow(['Average Number of Games Played per Month by Top 5 Juniors'])
		juniorGamesWriter.writerow([])
		juniorGradesWriter.writerow(['Average Rating of Top 5 Juniors'])
		juniorGradesWriter.writerow([])

		yearList_count = [0,0,0,0,0,0,0,0,0,0]
		gameList_count_boys = [0,0,0,0,0,0,0,0,0,0]
		gameList_count_std_boys = [0,0,0,0,0,0,0,0,0,0]
		ratingList_count_boys = [0,0,0,0,0,0,0,0,0,0]
		ratingList_count_std_boys = [0,0,0,0,0,0,0,0,0,0]
		gameList_count_girls = [0,0,0,0,0,0,0,0,0,0]
		gameList_count_std_girls = [0,0,0,0,0,0,0,0,0,0]
		ratingList_count_girls = [0,0,0,0,0,0,0,0,0,0]
		ratingList_count_std_girls = [0,0,0,0,0,0,0,0,0,0]

		# Loop over time and work out averages by each year
		for t in range(len(fed_.time)):
			# Find the year
			year = floor(fed_.time[t])

			# Find index for each year
			index_year = intYearList.index(year)

			# Add counts and data to list
			yearList_count[index_year] += 1
			gameList_count_boys[index_year] += fed_.games_boys_top5_mean[t]
			gameList_count_std_boys[index_year] += fed_.games_boys_top5_std[t]
			gameList_count_girls[index_year] += fed_.games_girls_top5_mean[t]
			gameList_count_std_girls[index_year] += fed_.games_girls_top5_std[t]
			ratingList_count_boys[index_year] += fed_.rating_boys_top5_mean[t]
			ratingList_count_std_boys[index_year] += fed_.rating_boys_top5_std[t]
			ratingList_count_girls[index_year] += fed_.rating_girls_top5_mean[t]
			ratingList_count_std_girls[index_year] += fed_.rating_girls_top5_std[t]

			# Total statistics
			if math.isnan( fed_.games_girls_top5_mean[t]) == False  and math.isnan( fed_.games_boys_top5_mean[t]) == False:
				yearList_count_all[index_year] += 1
				gameList_count_boys_all[index_year] += fed_.games_boys_top5_mean[t]
				gameList_count_girls_all[index_year] += fed_.games_girls_top5_mean[t]

		# Find average
		for y in range(len(yearList_count)):
			if yearList_count[y] > 0:
				gameList_count_boys[y] /= yearList_count[y]
				gameList_count_girls[y] /= yearList_count[y]
				ratingList_count_boys[y] /= yearList_count[y]
				ratingList_count_girls[y] /= yearList_count[y]
				gameList_count_std_boys[y] /= yearList_count[y]
				gameList_count_std_girls[y] /= yearList_count[y]
				ratingList_count_std_boys[y] /= yearList_count[y]
				ratingList_count_std_girls[y] /= yearList_count[y]
			else:
				gameList_count_boys[y] = 0.0
				gameList_count_girls[y] = 0.0
				ratingList_count_boys[y] = 0.0
				ratingList_count_girls[y] = 0.0
				gameList_count_std_boys[y] = 0.0
				gameList_count_std_girls[y] = 0.0
				ratingList_count_std_boys[y] = 0.0
				ratingList_count_std_girls[y] = 0.0

		# Write to file

		# Year
		juniorGamesWriter.writerow(yearList)
		juniorGradesWriter.writerow(yearList)
		# Average number of games
		juniorGamesWriter.writerow(['Games (boys)',gameList_count_boys])
		juniorGamesWriter.writerow(['Games s.d. (boys)',gameList_count_std_boys])
		juniorGamesWriter.writerow(['Games (girls)',gameList_count_girls])
		juniorGamesWriter.writerow(['Games s.d. (girls)',gameList_count_std_girls])
		# Average ratings
		juniorGradesWriter.writerow(['Rating (boys)',ratingList_count_boys])
		juniorGradesWriter.writerow(['Rating s.d. (boys)',ratingList_count_std_boys])
		juniorGradesWriter.writerow(['Rating (girls)',ratingList_count_girls])
		juniorGradesWriter.writerow(['Rating s.d. (girls)',ratingList_count_std_girls])

		# Plot
		plt.figure()
		#plt.title('Average Number of Games (Top 5 Juniors per Federation)',fontsize=20)
		plt.ylabel('Games',fontsize = 20)
		plt.xlabel('Year',fontsize = 20)
		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)
		plt.plot(intYearList,gameList_count_boys,label='M',color=[0, 145./255., 181./255.])
		plt.plot(intYearList,gameList_count_girls,label='F',color=[244./255., 170./255., 0])
		plt.legend(fontsize=14)
		plt.savefig(fedDirectory +'/JuniorGames'+fed_.name)
		#plt.show(block=False)
		plt.close()


		juniorGames.close()
		juniorGrades.close()
	print(gameList_count_girls_all)
	# Total Statistics
	for y in range(len(yearList_count_all)):
		if yearList_count_all[y] > 0:
			gameList_count_boys_all[y] /= yearList_count_all[y]
			gameList_count_girls_all[y] /= yearList_count_all[y]
		else:
			gameList_count_boys_all[y] += 0.0
			gameList_count_girls_all[y] += 0.0


			# Add year to array and consider previous year complete

		# Ratings of top 5 girls and boys
		# Plot rating Boys raw
		# Plot ratings Girls raw
		# Individually and on the same graph
		# y-axis 1500 - 2700
		# include only juniors with average rating > 1500

		# Write to file
		# Find number of games per year

		# Number of games  of top 5 girls and boys
		# on the same graph
		# y-axis 1500 - 2700
		# include only juniors with average rating > 1500

		# Write to file

		############################################################################
		# Disparity / Gap between men and womens chess

		# Difference between average_10 - average_women_10

	plt.title('Average Number of Games (Top 5 Juniors per Federation)',fontsize=20)
	plt.ylabel('Games',fontsize = 20)
	plt.xlabel('Year',fontsize = 20)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.plot(intYearList,gameList_count_boys_all,label='M',color=[0, 145./255., 181./255.])
	plt.plot(intYearList,gameList_count_girls_all,label='F',color=[244./255., 170./255., 0])
	plt.legend(fontsize=14)
	plt.savefig('../' +'/JuniorGamesAll.png')
	plt.show(block=False)
