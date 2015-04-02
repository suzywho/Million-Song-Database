## CS 2120 Assignment #1
## Name: Shi(Susan) Hu
## Student number: 250687453


def load_asn1_data(filename='songdata.csv'):
	
	import csv
	
	reader = csv.reader(open(filename, 'r'))
	songs = []
	
	for r in reader:
		songs.append(r)
		
	return songs
	
	
def fastest_year(songs):
	"""
	Function to find which year has the fastest song in the database.
	
	:param songs: A list of lists containing the song data
	
	:returns: An integer which is the year of the fastest song in the database.
	"""
	
	fastest_year=0		#variable for year of the fastest song
	fastest_tempo=0		#variable for the fastest tempo
	
	
	for song in songs[0:-2]:		#loop to iterate through the properties of the songs
			 
		year = int(song[2])			#variable for year of a song
		tempo = float(song[3])		#variable for tempo of a song
		
		if tempo>fastest_tempo:		#if the tempo of the current song is faster than the 
			fastest_tempo=tempo		#tempo recorded so far, the new, fastest tempo will be
			fastest_year=year		#stored
	return fastest_year				#return the year of the song with the fastest tempo
			


def loudest_song(songs):
	"""
	Function to find which song is the loudest in the database.
	
	:param songs: A list of lists containing the song data
	
	:returns: A string which is title of loudest song in the database.
	"""
	
	loudest_song=0					#variable for the loudest song
	song_name='SONG_IS_SO_LOUDDD'	#variable for the song name
	
	
	for song in songs[0:-2]:		#loop to iterate through the properties of the songs
	
		title = song[0]				#variable for title of the song
		loudness = float(song[7])	#variable for the loudness of a song
		
		if loudness>loudest_song:	#if the loudness of the current song is louder than the 
			loudest_song=loudness	#loudness recorded so far, the new, loudest song will be
			song_name=title 		#stored
	return song_name				#return the song name of the loudest song
	

def hottest_artist(songs):
	"""
	Function to find who is the hottest artist in the database.
	
	:param songs: A list of lists containing the song data
	
	:returns: An string which is the name of the hottest artist in the database.
	"""

	hotness=0						#variable for the popularity of the artist 
	hottest_artist='im_on_fire'		#variable for the most popular artist
	
	for song in songs[0:-2]:		#loop to iterate through the properties of the songs
	
		artist = song[1]			#variable for the artist name
		artist_hotness=float(song[4])#variable for the popularity of the artist
							
		if artist_hotness>hotness:	#if the popularity of the current artist is higher
			hotness=artist_hotness	#than the popularity of an artist recorded so far, the
			hottest_artist=artist	#most popular artist will be stored
	return hottest_artist			#return the name of the most popular artist 
	

	
# Load the songs and store them in a variable
songs =load_asn1_data(filename='songdata.csv')
# year with the fastest tempo
print fastest_year(songs);
# name of the loudest song
print loudest_song(songs);
# name of the hottest artist
print hottest_artist(songs);
