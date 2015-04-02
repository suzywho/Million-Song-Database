## CS 2120 Assignment #2 -- Zombie Apocalypse
## Name: Shi (Susan) Hu
## Student number: 250687453

import numpy
import pylab as P

#### This stuff you just have to use, you're not expected to know how it works.
#### You just need to read the plain English function headers.
#### If you want to learn more, by all means follow along (and ask questions if
#### you're curious). But you certainly don't have to.

def make_city(name,neighbours):
	"""
	Create a city (implemented as a list).
	
	:param name: String containing the city name
	:param neighbours: The city's row from an adjacency matrix.
	
	:return: [name, Infection status, List of neighbours]
	"""
	
	return [name, False, list(numpy.where(neighbours==1)[0])]
	

def make_connections(n,density=0.25):
	"""
	This function will return a random adjacency matrix of size
	n x n. You read the matrix like this:
	
	if matrix[2,7] = 1, then cities '2' and '7' are connected.
	if matrix[2,7] = 0, then the cities are _not_ connected.
	
	:param n: number of cities
	:param density: controls the ratio of 1s to 0s in the matrix
	
	:returns: an n x n adjacency matrix
	"""
	
	import networkx
	
	# Generate a random adjacency matrix and use it to build a networkx graph
	a=numpy.int32(numpy.triu((numpy.random.random_sample(size=(n,n))<density)))
	G=networkx.from_numpy_matrix(a)
	
	# If the network is 'not connected' (i.e., there are isolated nodes)
	# generate a new one. Keep doing this until we get a connected one.
	# Yes, there are more elegant ways to do this, but I'm demonstrating
	# while loops!
	while not networkx.is_connected(G):
		a=numpy.int32(numpy.triu((numpy.random.random_sample(size=(n,n))<density)))
		G=networkx.from_numpy_matrix(a)
	
	# Cities should be connected to themselves.
	numpy.fill_diagonal(a,1)
	
	return a + numpy.triu(a,1).T

def set_up_cities(names=['City 0', 'City 1', 'City 2', 'City 3', 'City 4', 'City 5', 'City 6', 'City 7', 'City 8', 'City 9', 'City 10', 'City 11', 'City 12', 'City 13', 'City 14', 'City 15']):
	"""
	Set up a collection of cities (world) for our simulator.
	Each city is a 3 element list, and our world will be a list of cities.
	
	:param names: A list with the names of the cities in the world.
	
	:return: a list of cities
	"""
	
	# Make an adjacency matrix describing how all the cities are connected.
	con = make_connections(len(names))
	
	# Add each city to the list
	city_list = []
	for n in enumerate(names):
		city_list += [ make_city(n[1],con[n[0]]) ]
	
	return city_list

def draw_world(world):
	"""
	Given a list of cities, produces a nice graph visualization. Infected
	cities are drawn as red nodes, clean cities as blue. Edges are drawn
	between neighbouring cities.
	
	:param world: a list of cities
	"""
	
	import networkx
	import matplotlib.pyplot as plt
	
	G = networkx.Graph()
	
	bluelist=[]
	redlist=[]
	
	plt.clf()
	
	# For each city, add a node to the graph and figure out if
	# the node should be red (infected) or blue (not infected)
	for city in enumerate(world):
		if city[1][1] == False:
			G.add_node(city[0])
			bluelist.append(city[0])
		else:
			G.add_node(city[0],node_color='r')
			redlist.append(city[0])
			
		for neighbour in city[1][2]:
			G.add_edge(city[0],neighbour)
	
	# Lay out the nodes of the graph
	position = networkx.circular_layout(G)
	
	# Draw the nodes
	networkx.draw_networkx_nodes(G,position,nodelist=bluelist, node_color="b")
	networkx.draw_networkx_nodes(G,position,nodelist=redlist, node_color="r")

	# Draw the edges and labels
	networkx.draw_networkx_edges(G,position)
	networkx.draw_networkx_labels(G,position)

	# Force Python to display the updated graph
	plt.show()
	plt.draw()
	
def print_world(world):
	"""
	In case the graphics don't work for you, this function will print
	out the current state of the world as text.
	
	:param world: a list of cities
	"""
	
	import string
	
	print string.ljust('City',15), 'Zombies?'
	print '------------------------'
	for city in world:
		print string.ljust(city[0],15), city[1]



#### That's the end of the stuff provided for you.
#### Put *your* code after this comment.

#Zombify the chosen city in the list of cities
def zombify(cities,cityno):
	#Set the infected property to True
	cities[cityno][1] = True

#Cure the chosen city in the list of cities
def cure(cities,cityno):
	#Make sure that the zeroth city is not cured
	if (cityno != 0):
		#Set the infected property to True
		cities[cityno][1] = False

#Do one simulation of the zombie plague based on the values of p_spread and p_cure
def sim_step(cities,p_spread,p_cure):
	#counter to keep track of the index of the city
	counter = 0;
	#Iterate through every city in the list of cities
	for city in cities:
		#If the city is infected , infect one of its neighbour
   		if city[1] and numpy.random.rand() < p_spread:
   			no_of_neighbours = len(city[2]) 
   			#Generate random index based on the length of the neighbour
   			random_city = city[2][numpy.random.randint(0, no_of_neighbours)] 
   			#Zombify the random city
   			zombify(cities,random_city)
	   	
	   	#If the city is infected , attemp to cure it
	   	if city[1] and numpy.random.rand() < p_cure:
	   		#Cure the current city
			cure(cities,counter)
			
		counter += 1

#Function to check whether it is the end of the world
def is_end_of_world(cities):
	#Iterate through every city in the list of cities
	for city in cities:
		if not(city[1]):
			#Return False if the city is not infected
			return False
	#Return true if the loop didnt find any cured cities
	return True

#Function that counts how many steps it takes to reach the end of the world
def time_to_end_of_world(p_spread,p_cure):
	#Sets up city
	world = set_up_cities()
	#Infect world 0 since it is always infected
	zombify(world,0)
	#Counter to keep track of the number of days it takes
	day_counter = 0
	#Simulate another step and count the days while its not the end of the world
	while not(is_end_of_world(world)):
		sim_step(world, p_spread, p_cure)
		day_counter += 1
	return day_counter

#Execute time_to_end_of_world n times
def end_world_many_times(n,p_spread,p_cure):
	times_to_the_end_of_the_world = []
	for x in range(0, n):
		#Appends the number of days to a list to be returned
		times_to_the_end_of_the_world.append(time_to_end_of_world(p_spread,p_cure))
		print x

	return times_to_the_end_of_the_world

#Graphing code
ttl = end_world_many_times(500, 1, 0)
P.hist(ttl)
P.ylabel("Number Per Bin")
P.xlabel("Number of Days")
P.show()
