# Plots statistics
import os
import glob
import numpy as np
import csv
import matplotlib as plt

outputDataDir = '../dataAllYears'

# Find path
fileList = glob.glob(outputDataDir+'/*Stats.csv')

monthList = ['Jan','Feb','March','April','May','June','July','Aug','Sep','Oct','Nov','Dec']

class monthYearStats:
	def __init__(self,Time,Players,Inactive,Arbiters,Trainers,Players1800,Players2100):
		self.Time = Time						  # time
		self.Players = Players                    # [All,Women,Men]
		self.Inactive = Inactive                  # [All,Women]
		self.Arbiters = Arbiters                  # [All,Women]
		self.Trainers = Trainers                  # [All,Women]
		self.Players1800 = Players1800            # [All,All inactive, Women, Women inactive]
		self.Players2100 = Players2100			  # [All,All inactive, Women, Women inactive]
def extractMonthYearStats(file,time):
	# Read csv
	with open(file, newline='') as f:
		reader = csv.reader(f)
		rows = list(reader)

		# Find data from file
		players = [rows[2][1],rows[3][1],rows[4][1]]
		inactive = [rows[5][1],rows[6][1]]
		arbiters = [rows[8][1],rows[9][1]]
		trainers = [rows[10][1],rows[11][1]]
		players1800 = [rows[13][1],rows[14][1],rows[15][1],rows[16][1]]
		players2100 = [rows[17][1],rows[18][1],rows[19][1],rows[20][1]]

		# Sort data into object
		object = monthYearStats(time,players,inactive,arbiters,trainers,players1800,players2100)



for file in fileList:
	# Find month and year of files
	split = file.split('/')[2]
	split = split.split('Stats')[0]
	year = split[-4:]
	month = split[:-4]

	# Convert month to fraction of year (to make time indicator)
	time = float(year) + float(monthList.index(month)/12)

	extractMonthYearStats(file,time)


#print(filenames)
#for path in pathYM:
#	# Find year and month
#	splitYM = path.split('/')
#	year = splitYM[1]
#	month = splitYM[2]
#	print('extracting : ',month, year)
#
#	# Find filepaths
#	filepath = glob.glob('../'+year+'/'+month+'/'+'*.txt')[0] # input
#	outfileName = outputDir+'/'+month+year+'.csv'             # output
#	outdatafileName = outputDataDir+'/'+month+year+'Stats'+'.csv'
