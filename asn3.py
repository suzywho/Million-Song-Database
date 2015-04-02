## CS 2120 Assignment #3
## Name: Shi (Susan) Hu
## Student number: 250687453

import numpy
import pylab
import math
import scipy.io as io
import scipy.stats as stats

def loaddata(filename):
	"""
	This function loads and reads the file `a3data.csv` 

	:returns a LIST of of lists
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
	the correct data types. Additionally, it ignores the first column

	:returns: A 2d array of the passed data ignoring the first column 
			  and converts all columns to floats except the last columns
			  which is converted to an int
	"""
	filtered_array = []
	counter = 0

	for val in datalist:
		#make a new row for every data set
		filtered_array.append([])

		#change the type to the appropriate types
		filtered_array[counter].append(val[1].astype(numpy.float))
		filtered_array[counter].append(val[2].astype(numpy.float))
		filtered_array[counter].append(val[3].astype(numpy.float))
		filtered_array[counter].append(val[4].astype(numpy.float))
		filtered_array[counter].append(val[5].astype(numpy.float))
		filtered_array[counter].append(val[6].astype(numpy.float))
		filtered_array[counter].append(val[7].astype(numpy.int))
		counter += 1

	return filtered_array

def save_array(arr, fname):
	"""
	This function saves the given array into a matlab file with the given name
	"""
	dictionary = {}
	dictionary['vampire_array'] = arr
	io.savemat(fname, dictionary)
	return

def column_stats(arr, col):
	"""
	This function process the min max and mean for a specific columns for vampires and
	normal humans

	:returns: A 2d array with the mean min and max of the  vampires in the zero index 
			and the mean min and max of normal humans in the first index 
	"""

	#Counter to keep track of total vampires
	vampire_counter = 0
	#Counter to keep track of total normal humans
	normal_counter = 0

	#variables to keep track of vampirestats
	vampire_mean = 0
	vampire_min = 9999999999
	vampire_max = -999999999

	#variables to keep track of human stats
	normal_mean = 0
	normal_min = 9999999999
	normal_max = -999999999

	vampire_stats = []
	normal_stats = []
	all_stats = []

	for val in arr:
		#Calculate vampire stats
		if (val[6] == 1):
			vampire_mean += val[col]
			vampire_counter += 1
			if (val[col] > vampire_max):
				vampire_max = val[col]
			if (val[col] < vampire_min):
				vampire_min = val[col]

		#Calculate normal stats
		if (val[6] == 0):
			normal_mean += val[col]
			normal_counter += 1
			if (val[col] > normal_max):
				normal_max = val[col]
			if (val[col] < normal_min):
				normal_min = val[col]

	#Add the specific vampire stats to the array of vampire stats
	vampire_stats.append(vampire_mean/(vampire_counter))
	vampire_stats.append(vampire_min)
	vampire_stats.append(vampire_max)

	#Add the specific human stats to the array of human stats
	normal_stats.append(normal_mean/normal_counter)
	normal_stats.append(normal_min)
	normal_stats.append(normal_max)

	#Aggregate the stats into one array
	all_stats.append(vampire_stats)
	all_stats.append(normal_stats)

	return all_stats

def  hist_compare(arr,col):
	"""
	This function plots two histograms allowing you to compare vampire and human stats
	"""
	plot_values = column_stats(arr, col)
	pylab.hist(plot_values[0])
	pylab.ylabel("Y")
	pylab.xlabel("X")
	pylab.show()
	pylab.hist(plot_values[1])
	pylab.ylabel("Y")
	pylab.xlabel("X")
	pylab.show()
	return

def corr_column(arr, col1, col2):
	"""
	This function calculates the pearson correlation value between 2 columns of the
	given data set

	:returns: 2 tailed pearson r value
	"""
	col_one = get_column(arr, col1)
	col_two = get_column(arr, col2)
	r = stats.pearsonr(col_one, col_two)
	return r

def scatter_columns(arr,col1,col2):
	"""
	This function plots a scatter plot of the two columns of the dataset
	"""
	col_one = get_column(arr, col1)
	col_two = get_column(arr, col2)
	pylab.scatter(col_one, col_two)
	pylab.ylabel("Y")
	pylab.xlabel("X")
	pylab.show()

	return

def is_vampire(row, stake_stats, garlic_stats, reflect_stats, shiny_stats):
	"""
	This function calculates the probability that the given data points to a 
	vampire

	:returns: A probability between 0.0001 and 0.9999
	"""
	#ensures that the probability can never be smaller thatn 0.0001
	p = 0.0001

	#For my calculations, I only needed the mean of the following stats
	vampire_stake_mean = stake_stats[0][0]
	vampire_shiny_stats = shiny_stats[0][0]
	vampire_garlic_stats = garlic_stats[0][0]
	vampire_reflect_stats = reflect_stats[0][0]

	#Calculating the percentile difference between the mean and the actual value

	#These qualities were weight in terms of importance
	#Stake Aversion was weighed 70%
	#Garlic Aversion was weighed 10%
	#Reflectance was weighed 10%
	#Shiny was weighed 10%

	p += (1 - (math.fabs(vampire_stake_mean - row[3])/vampire_stake_mean)) * 0.7
	p += (1 - (math.fabs(vampire_garlic_stats - row[4])/vampire_garlic_stats)) * 0.1
	p += (1 - (math.fabs(vampire_reflect_stats - row[5])/vampire_reflect_stats)) * 0.1
	p += (1 - (math.fabs(vampire_shiny_stats - row[6])/vampire_shiny_stats)) * 0.1
	
	
	#Ensure that the probablity never goes above 0.9999
	if (p > 1):
		p = 0.9999

	return p

def log_likelihood(arr,vampire_function):
	"""
	Calcuates the likelihood of the passed statistical model
	:returns: The likelihood of the passed statistical model
	"""
	stake_stats = column_stats(data, 2)
	garlic_stats = column_stats(data, 3)
	reflect_stats = column_stats(data, 4)
	shiny_stats = column_stats(data, 5)

	likelihood = 0.0

	for val in arr:
		prob = vampire_function(val, stake_stats, garlic_stats, reflect_stats, shiny_stats)
		if (val[6].astype(numpy.int) == 0):
			if (prob > 0.5):
				prob = 1 - prob

		likelihood = likelihood * prob

	return likelihood

def percent_correct (arr, vampire_function):
	"""
	Calcuates the number of correct answers for a given data set
	:returns: The percentage of correct answers
	"""
	stake_stats = column_stats(arr, 3)
	garlic_stats = column_stats(arr, 4)
	reflect_stats = column_stats(arr, 5)
	shiny_stats = column_stats(arr, 6)

	right = 0.0
	total = 0.0

	for val in arr:
		prob = vampire_function(val, stake_stats, garlic_stats, reflect_stats, shiny_stats)
		if (val[6].astype(numpy.int) == 1 and prob > 0.5):
			right += 1
		if (val[6].astype(numpy.int) == 0 and prob < 0.5):
			right += 1

		total += 1


	return (right/total) * 100

def get_column (arr, col):
	"""
	This function returns the column for a given array
	I was getting the following error : list indices must be integers, not tuple
	when trying to use arr[:,col] so I wrote this as a workaround for now
	"""

	col_arr = []
	for val in arr:
		col_arr.append(val[col])

	return col_arr

data = loaddata('a3data.csv');
data = numpy.array(data)  
data = dat2arr(data)
save_array(data, 'test')

