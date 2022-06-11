# ...
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

def plotmeanDev(file):
	f = open(file, "r")

	yearList = []
	meanList = []
	stdList = []
	# Loop through file
	while f:
		line = f.readline()
		if line.split(' ')[0] == 'December':
			yearList.append(int(line.split(' ')[1]))
			meanList.append(float(f.readline().split(',')[1][0:8]))
			stdList.append(float(f.readline().split(',')[1][0:8]))
		# if end of file reached
		if (not line):
			break

	plt.title('Average Rating Difference Between the Top 10 Men and Women (Federation)',fontsize=20)
	plt.ylabel('Difference',fontsize=20)
	plt.xlabel('Year',fontsize = 20)
	plt.xlim(2011.8,2021.2)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.plot(yearList,meanList)
	plt.savefig('Ratingdifferene')
	plt.show()

def plotCategories(file):
	f = open(file, "r")

	yearList = []
	# Number of federations in each category
	AList = []
	BList = []
	CList = []
	DList = []
	EList = []
	FList = []
	GList = []

	# Loop through file
	while f:
		line = f.readline()

		if line.split(' ')[0] == 'December':
			# Find year
			yearList.append(int(line.split(' ')[1]))

			# Skip over unwanted rows
			for i in range(4):
				line = f.readline()

			# Initialise category counts
			A = 0
			B = 0
			C = 0
			D = 0
			E = 0
			F = 0
			G = 0

			# Loop through years data
			yearFlag = True
			while yearFlag:

				line = f.readline()

				# Stop at end of year
				if len(line) == 1:
					yearFlag = False

				# Count number in categories
				else:
					line = line.split(',')[6]
					category = line.split()[0]
					if category == 'A':
						A += 1
					if category == 'B':
						B += 1
					if category == 'C':
						C += 1
					if category == 'D':
						D += 1
					if category == 'E':
						E += 1
					if category == 'F':
						F += 1
					if category == 'G':
						G += 1

			# Add counts to list for each year
			AList.append(A)
			BList.append(B)
			CList.append(C)
			DList.append(D)
			EList.append(E)
			FList.append(F)
			GList.append(G)

		# if end of file reached
		if (not line):
			break

	# Plot
	plt.title('Rating Difference Categories',fontsize=20)
	plt.ylabel('Number of Federations',fontsize=20)
	plt.xlabel('Year',fontsize = 20)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.xlim(2011.8,2021.2)
	plt.plot(yearList,AList,label='A')
	plt.plot(yearList,BList,label='B')
	plt.plot(yearList,CList,label='C')
	plt.plot(yearList,DList,label='D')
	plt.plot(yearList,EList,label='E')
	plt.plot(yearList,FList,label='F')
	plt.plot(yearList,GList,label='G')
	plt.legend(fontsize=18)
	plt.savefig('Categories')
	plt.show()

def plotTopRatingDiffCorr(file):
	f = open(file, "r")

	yearList = []
	ratingDiffList = []
	MenRankingsList = []
	WomenRankingsList = []

	# Loop through file
	while f:
		line = f.readline()

		if line.split(' ')[0] == 'December' and int(line.split(' ')[1]) == 2021:
			# Find year
			yearList.append(int(line.split(' ')[1]))

			# Skip over unwanted rows
			for i in range(4):
				line = f.readline()

			# Loop through years data
			yearFlag = True
			while yearFlag:

				line = f.readline()
				print(line)

				# Stop at end of year
				if len(line) == 1:
					yearFlag = False

				# Count number in categories
				else:
					MenRankingsList.append(float(line.split(',')[2]))
					WomenRankingsList.append(float(line.split(',')[3]))
					ratingDiffList.append(float(line.split(',')[4]))

		# if end of file reached
		if (not line):
			break

	print(WomenRankingsList)

	# Plot
	plt.title('Correlation Between Stongest Federations and Rating Differences',fontsize=20)
	plt.ylabel('Rating Difference',fontsize=20)
	plt.xlabel('Rating (Average of Top 10)',fontsize = 20)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.xlim(2750,2000)
	plt.scatter(MenRankingsList,ratingDiffList,s=10)
	#plt.legend(fontsize=18)
	plt.savefig('CorrelationDiff')
	plt.show()

	# Plot
	plt.title('Correlation Between Stongest Federations (Women) and Rating Differences',fontsize=20)
	plt.ylabel('Rating Difference',fontsize=20)
	plt.xlabel('Rating (Average of Top 10 Women)',fontsize = 20)
	plt.xticks(fontsize=18)
	plt.yticks(fontsize=18)
	plt.xlim(2450,1400)
	plt.scatter(WomenRankingsList,ratingDiffList,s=10)
	#plt.legend(fontsize=18)
	plt.savefig('CorrelationDiffWomen')
	plt.show()

################################################################################
# Main

file = '../topFederations/disparityMetric.csv'
#plotmeanDev(file)
#plotCategories(file)
plotTopRatingDiffCorr(file)
