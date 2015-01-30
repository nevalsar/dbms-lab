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

def insertMovie(movie_id, movie):
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

def getMovieID(pageCount):
    for i in range(pageCount):

		listPage = "http://www.imdb.com/search/title?languages=hi|1&num_votes=50,&sort=user_rating,desc&start=" + str(i * 50) + "&title_type=feature"
		print listPage
		doc = lxml.html.document_fromstring(requests.get(listPage).content)
		movies_list = doc.find_class("results")[0].findall("tr")[1:]

		for movie in movies_list:
			movie_name = movie.findall("td")[2].find("a").text_content()
			movie_id = movie.findall("td")[2].find("a").get("href")[7:-1]
			movie_link = 'http://imdb.com/title/' + movie_id
			print movie_name, movie_link
			movie = getMovie(movie_id)
			insertMovie(movie_id, movie)

if __name__ == "__main__":
    getMovieID(1)
