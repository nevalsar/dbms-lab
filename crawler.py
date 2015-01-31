import sys
import requests
import lxml.html
import MySQLdb as db

#sudo pip install requests==1.2.3 lxml==3.2.1

def getMovie(id):
	hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + id).content)
	movie = {}
	try:
		movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
	except IndexError:
		movie['title']
	try:
		movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
	except IndexError:
		try:
			movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
		except IndexError:
			movie['year'] = ""
	try:
		movie['certification'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[1]/@title')[0].strip()
	except IndexError:
		movie['certification'] = ""
	try:
		movie['running_time'] = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
	except IndexError:
		movie['running_time'] = ""
	try:
		movie['genre'] = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
	except IndexError:
		movie['genre'] = []
	try:
		movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
	except IndexError:
		try:
			movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
		except Exception:
			movie['release_date'] = ""
	try:
		movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
	except IndexError:
		movie['rating'] = ""
	try:
		movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
	except IndexError:
		movie['metascore'] = 0
	try:
		movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
	except IndexError:
		movie['description'] = ""
	try:
		movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
	except IndexError:
		movie['director'] = ""
	try:
		movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
	except IndexError:
		movie['stars'] = ""
	try:
		movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
	except IndexError:
		movie['poster'] = ""
	try:
		movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
	except IndexError:
		movie['gallery'] = ""
	try:
		movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
	except IndexError:
		movie['storyline'] = ""
	try:
		movie['votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
	except IndexError:
		movie['votes'] = ""
	return movie

def insertMovie(movie_id):
	movie = getMovie(movie_id)
	con = db.connect('localhost', 'root', 'root', 'imdb');

	with con:
	    cur = con.cursor()
	    query = "INSERT INTO Movie(MID, title, year, rating, num_votes) VALUES("\
	    		+ "'" + movie_id 			+ "', "\
	    		+ "'" + movie['title'] 		+ "', "\
	    		+ "'" + movie['year'] 		+ "', "\
	    		+ "'" + movie['rating'] 	+ "', "\
	    		+ "'" + movie['votes'] 		+ "'"\
	    		+ ")";\
		print query
	    cur.execute(query)

def getPerson(person_id):
	doc = lxml.html.document_fromstring(requests.get("http://www.imdb.com/name/" + str(person_id)).content)
	person = {}

	try:
		person['name'] = doc.get_element_by_id("overview-top").find_class("header")[0].find("span").text_content()
	except IndexError:
		person['name'] = ""
	try:
		person['dob'] = doc.get_element_by_id("name-born-info").find("time").get("datetime")
	except (IndexError, KeyError, AttributeError):
		person['dob'] = ""
	try:
		person['gender'] = doc.get_element_by_id("name-job-categories").find("a").find("span").text_content().strip()
		person['gender'] = ('F', 'M')[person['gender'] == 'Actor']
	except IndexError:
		person['gender'] = ""

	return person

def insertPerson(person_id):
	person = getPerson(person_id)
	con = db.connect('localhost', 'root', 'root', 'imdb');

	with con:
	    cur = con.cursor()
	    query = "INSERT INTO Person(PID, Name, DOB, Gender) VALUES("\
	    		+ "'" + person_id 			+ "', "\
	    		+ "'" + person['name'] 		+ "', "\
	    		+ "'" + person['dob'] 		+ "', "\
	    		+ "'" + person['gender'] 		+ "'"\
	    		+ ")";\
		print query
	    cur.execute(query)

def insertGenre(genre_name):
	con = db.connect('localhost', 'root', 'root', 'imdb');

	with con:
	    cur = con.cursor()
	    query = "INSERT INTO Genre(Name) VALUES("\
	    		+ "'" + genre_name 		+ "'"\
	    		+ ")";\
		print query
	    cur.execute(query)

def getMovieID(pageCount):
    for i in range(pageCount):

		listPage = "http://www.imdb.com/search/title?languages=hi|1&num_votes=50,&sort=user_rating,desc&start=" + str(i * 50) + "&title_type=feature"
		page_top_movies = lxml.html.document_fromstring(requests.get(listPage).content)
		list_top_movies = page_top_movies.find_class("results")[0].findall("tr")
		list_top_movies[:] = [movie.findall("td")[2].find("a").get("href")[7:-1] for movie in list_top_movies if len(movie.findall("td"))>2]

		for movie_id in list_top_movies:
			insertMovie(movie_id)
			page_movie = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + movie_id + "/fullcredits").content)

			list_actors = page_movie.find_class("cast_list")[0].findall("tr")
			list_actors[:] = [actor.findall("td")[1].find("a").get("href")[6:15] for actor in list_actors if len(actor.findall("td"))>1]
			for actor_id in list_actors:
				insertPerson(actor_id)

			page_movie = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + movie_id).content)
			list_genres = page_movie.find_class("infobar")[0].findall("a")
			list_genres[:] = [a.find("span").text_content() for a in list_genres]

			for genre in list_genres:
				insertGenre(genre);

if __name__ == "__main__":
    getMovieID(1)
