# Plots statistics
import os
import glob
import numpy as np
import csv
import matplotlib.pyplot as plt
import shendrukGroupFormat as ed
from matplotlib.colors import LinearSegmentedColormap as lsc
from pylab import *
plt.style.use('shendrukGroupStyle')
#plt.style.use('shendrukGroupStyle')

outputDataDir = '../dataAllYears'

# Find path
fileList = glob.glob(outputDataDir+'/*Stats.csv')

monthList = ['Jan','Feb','March','April','May','June','July','Aug','Sep','Oct','Nov','Dec']

class monthYearStats:
	def __init__(self,Time,Players,Inactive,Arbiters,Trainers,Players1800,Players2100,Age):
		self.Time = Time						  # time
		self.Players = Players                    # [All,Women,Men]
		self.Inactive = Inactive                  # [All,Women]
		self.Arbiters = Arbiters                  # [All,Women]
		self.Trainers = Trainers                  # [All,Women]
		self.Players1800 = Players1800            # [All,All inactive, Women, Women inactive]
		self.Players2100 = Players2100			  # [All,All inactive, Women, Women inactive]
		self.Age = Age							  # [[5-10],[10-20],...,[95-100]]
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

		ageList = []
		for i in range(20):
			ageList.append(rows[23+i][2])


		if players[0] != str(0):
			# Sort data into object
			object = monthYearStats(time,players,inactive,arbiters,trainers,players1800,players2100,ageList)
		else:
			object = 'none'
	f.close()
	return object


objectList = []

for file in fileList:
	# Find month and year of files
	split = file.split('/')[2]
	split = split.split('Stats')[0]
	year = split[-4:]
	month = split[:-4]

	# Convert month to fraction of year (to make time indicator)
	time = float(year) + float(monthList.index(month)/12)

	object = extractMonthYearStats(file,time)
	if object != 'none':						# None is flag that the number of players came out as zero (there was an error)
		objectList.append(object)
		print("Error in number of players")

# Order objects (months) by time (earliest --> latest)
objectList.sort(key=lambda x: x.Time)

# Plot figures
totalTime = []
totalPlayers = [[],[],[]]
totalInactive = [[],[]]
totalTrainers = [[],[]]
total1800 = [[],[],[],[]]
total2100 = [[],[],[],[]]
totalAge = []


for obj in objectList:
	# Time
	totalTime.append(obj.Time)

	# Total Players
	totalPlayers[0].append(float(obj.Players[0]))
	totalPlayers[1].append(float(obj.Players[1]))
	totalPlayers[2].append(float(obj.Players[2]))

	# Total Inactive
	totalInactive[0].append(float(obj.Inactive[0]))
	totalInactive[1].append(float(obj.Inactive[1]))

	# Total Trainers
	totalTrainers[0].append(float(obj.Trainers[0]))
	totalTrainers[1].append(float(obj.Trainers[1]))

	# Total Players > 1800
	total1800[0].append(float(obj.Players1800[0]))
	total1800[1].append(float(obj.Players1800[1]))
	total1800[2].append(float(obj.Players1800[2]))
	total1800[3].append(float(obj.Players1800[3]))

	# Total Players > 1800
	total2100[0].append(float(obj.Players2100[0]))
	total2100[1].append(float(obj.Players2100[1]))
	total2100[2].append(float(obj.Players2100[2]))
	total2100[3].append(float(obj.Players2100[3]))

	totalAge.append(obj.Age)
	#totalAge.append(float(obj.Age))


percentagePlayers = [[],[]] # % of female or male players as proportion of total players
percentage1800 = [[],[]] # % of female players > 1800 as proportion of total players > 1800
percentage2100 = [[],[]] # % of female players > 1800 as proportion of total players > 1800
percentageTrainers = []
percentageInactive = []

for i in range(len(totalTime)):
	percentagePlayers[0].append(100*totalPlayers[1][i]/totalPlayers[0][i])
	percentagePlayers[1].append(100*totalPlayers[2][i]/totalPlayers[0][i])

	percentage1800[0].append(100*total1800[2][i]/total1800[0][i])
	percentage1800[1].append(100*total1800[3][i]/total1800[1][i])

	percentage2100[0].append(100*total2100[2][i]/total2100[0][i])
	percentage2100[1].append(100*total2100[3][i]/total2100[1][i])

	percentageTrainers.append(100*totalTrainers[1][i]/totalTrainers[0][i])

	percentageInactive.append(100*totalInactive[1][i]/totalInactive[0][i])

#print(totalTime)
#print(totalPlayers[1])

cerulean = [0, 145./255., 181./255.]

# Percentage women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,totalPlayers[1],color=cerulean)
plt.savefig('WomenNumber')
plt.show()

# Percentage women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,totalPlayers[0])
plt.savefig('Number')
plt.show()

# Percentage women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentagePlayers[0],color=cerulean)
plt.savefig('WomenFraction')
plt.show()

# Percentage inactive
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentageInactive,color=cerulean)
plt.savefig('WomenInactiveFraction')
plt.show()

# Percentage trainers women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentageTrainers,color=cerulean)
plt.savefig('WomenTrainersFraction')
plt.show()

# Percentage trainers women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,totalTrainers[1],color=cerulean)
plt.savefig('WomenTrainersNumber')
plt.show()

# Percentage trainers women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,totalTrainers[0])
plt.savefig('TrainersNumber')
plt.show()

# Percentage 1800 women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentage1800[0],color=cerulean)
plt.savefig('Women1800Fraction')
plt.show()


# Percentage 1800 women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentage1800[1],color=cerulean)
plt.savefig('Women1800InactiveFraction')
plt.show()

# Percentage 1800 women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentage2100[0],color=cerulean)
plt.savefig('Women2100Fraction')
plt.show()

# Number 1800 women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,total1800[2],color=cerulean)
plt.savefig('Women1800Number')
plt.show()

# Number 1800 women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,total1800[0])
plt.savefig('1800Number')
plt.show()

# Number 1800 women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,total2100[0])
plt.savefig('2100Number')
plt.show()

# Number 2100 women
plt.ylabel('Number of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,total2100[2],color=cerulean)
plt.savefig('Women2100Number')
plt.show()

# Percentage 1800 women
plt.ylabel('\% of Players')
plt.xlabel('Year')
plt.xlim(2012,2022)
plt.plot(totalTime,percentage2100[1],color=cerulean)
plt.savefig('Women2100InactiveFraction')
plt.show()
