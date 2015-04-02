## CS 2120 Assignment #4
## Name: Susan Hu
## Student number: 250687453

import numpy
import pylab
import math
import matplotlib.pyplot as plt

def loaddata(filename):
	"""
	This function loads and reads the file `movies.csv` 

	:returns a list of lists
	"""
	import csv

	reader = csv.reader(open(filename, 'r'))
	data = []
	
	for r in reader:
		data.append(r)
		
	return data

def dat2arr(datalist):
	"""
	This function takes in a list of data and returns a 2d array with
	the correct data types. Addiotionally, it ignores the first column

	:returns: A 2d array of the passed data ignoring the columns that are
	not listed
	"""
	filtered_array = []
	counter = 0

	for val in datalist:
		#make a new row for every data set
		filtered_array.append([])

		#change the type to the appropriate types
		filtered_array[counter].append(val[1]) #TITLE
		filtered_array[counter].append(val[3]) #LENGTH
		filtered_array[counter].append(val[4]) #BUDGET
		filtered_array[counter].append(val[5]) #RATING

		filtered_array[counter].append(val[18]) #ACTION
		filtered_array[counter].append(val[19]) #ANIMATION
		filtered_array[counter].append(val[20]) #COMEDY
		filtered_array[counter].append(val[21]) #DRAMA
		filtered_array[counter].append(val[22])	#DOCUMENTARY
		filtered_array[counter].append(val[23]) #ROMANCE
		filtered_array[counter].append(val[24]) #SHORT
		counter += 1

	return filtered_array

def find_average(arr, data_header, col):
	"""
	Finds the average for a specific column and a genre

	return: Returns the average for the specific columns for a genre
	"""
	mean = 0
	counter = 0

	for val in arr:
		if (val[col] == '1'):
			mean += val[data_header].astype(numpy.float)
			counter += 1

	return (mean/counter)

def average_time(data):
	"""
	Given the data, this function will return the average length per
	category

	return: returns a dict containing the average time per genre
	"""
	average_lengths = {}
	average_lengths['action'] = find_average (data, 1, 4)
	average_lengths['animation'] = find_average (data, 1, 5)
	average_lengths['comedy'] = find_average (data, 1, 6)
	average_lengths['drama'] = find_average (data, 1, 7)
	average_lengths['documentary'] = find_average (data, 1, 8)
	average_lengths['romance'] = find_average (data, 1, 9)
	average_lengths['short'] = find_average (data, 1, 10)

	return average_lengths

def average_rating(data):
	"""
	Given the data, this function will return the average rating per
	category

	return: returns a dict containing the average rating per genre
	"""
	average_ratings = {}
	average_ratings['action'] = find_average (data, 3, 4)
	average_ratings['animation'] = find_average (data, 3, 5)
	average_ratings['comedy'] = find_average (data, 3, 6)
	average_ratings['drama'] = find_average (data, 3, 7)
	average_ratings['documentary'] = find_average (data, 3, 8)
	average_ratings['romance'] = find_average (data, 3, 9)
	average_ratings['short'] = find_average (data, 3, 10)

	return average_ratings

def viz1(data):
	"""
	This visualization plots the average time per specific genre for a movie
	From here, we can see which movies generally run the longest
	"""
	D = average_time(data)
	plt.bar(range(len(D)), D.values(), align='center')
	plt.xticks(range(len(D)), D.keys())
	plt.show()

def viz2(data):
	"""
	This visualization plots the average rating per specific genre for a movie
	From here, we can see which movie genres are rated the highest
	"""
	D = average_rating(data)
	plt.bar(range(len(D)), D.values(), align='center')
	plt.xticks(range(len(D)), D.keys())
	plt.show()

#['$1000 a Touchdown', '71', 'NA', '6', '0', '0', '1', '0', '0', '0', '0']
#0: Title
#1: Length
#2: Budget
#3: Rating
#4: Action
#5: Animation
#6: Comedy
#7: Drama
#8: Documentary
#9: Romance
#10: Short

def classify_movie(data, length):
	"""
	Based on the length of the movie, this function will try
	its best to classify it into a genre

	returns: The best classification based on the length given
	"""
	average_times = average_time(data)
	genre_guess = ''
	length_difference = 99999

	for key in average_times:
		if (math.fabs(average_times[key] - length) < length_difference):
			genre_guess = key
			length_difference = math.fabs(average_times[key] - length)

	return genre_guess


data = loaddata('movies.csv');
data = numpy.array(data)  
data = dat2arr(data)


viz1(data)
viz2(data)

#Example classification of a movie
#classify_movie(data, 2))

