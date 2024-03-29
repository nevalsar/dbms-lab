# #####################################################
# Name             : NEVIN VALSARAJ
# Roll No         : 12CS10032
# Assignment     : DBMS Lab (cs43002) - Assignment 3
# Date             : 1 FEB 2105
# #####################################################

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
        votes = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
        movie['votes'] = votes.replace(',', '')
    except IndexError:
        movie['votes'] = ""
    return movie

def insertMovie(movie_id, movie):
    con = db.connect('localhost', 'root', 'root', 'imdb');

    with con:
        cur = con.cursor()
        query = "SELECT * FROM Movie WHERE MID = '" + movie_id + "';"
        print query
        cur.execute(query)

        if cur.fetchone() is not None:
            query = "INSERT INTO " + tablePrefix + "_Movie(MID, title, year, rating, num_votes) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + movie['title']         + "', "\
                + "'" + movie['year']         + "', "\
                + "'" + movie['rating']     + "', "\
                + "'" + movie['votes']         + "'"\
                + ")";\
            print query
            cur.execute(query)
        else:
            print "Movie exists in table Movie"

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
        person['gender'] = 'M'
        list_jobs = doc.get_element_by_id("name-job-categories").findall("a")
        for element in list_jobs:
            if 'Actress' in element.find("span").text_content().strip():
                person['gender'] = 'F'
    except IndexError:
        person['gender'] = ""

    return person

def insertPerson(person_id):
    person = getPerson(person_id)
    con = db.connect('localhost', 'root', 'root', 'imdb');

    with con:
        cur = con.cursor()
        query = "SELECT * from Person WHERE PID = '" + person_id + "';"
        cur.execute(query)

        if cur.fetchone() is not None:
            query = "INSERT INTO " + tablePrefix + "_Person(PID, Name, DOB, Gender) VALUES("\
                    + "'" + person_id             + "', "\
                    + "'" + person['name']         + "', "\
                    + "'" + person['dob']         + "', "\
                    + "'" + person['gender']         + "'"\
                    + ")";\
            print query
            cur.execute(query)
        else:
            print "Person already exist in Person"

def getGenres(page_movie):
    list_genres = page_movie.find_class("info")
    list_genres[:] = [a.find('div') for a in list_genres if 'Genre' in a.find('h5').text_content()]
    list_genres[:] = list_genres[0].findall('a')
    list_genres[:] = [a.text_content() for a in list_genres]
    return list_genres

def insertGenre(genre_name):
    con = db.connect('localhost', 'root', 'root', 'imdb');

    with con:
        cur = con.cursor()
        query = "SELECT * FROM Genre WHERE Name = '" + genre_name + "';"
        cur.execute(query)

        if cur.fetchone() is not None:
            query = "INSERT INTO " + tablePrefix + "_Genre(Name) VALUES("\
                    + "'" + genre_name         + "'"\
                    + ")";\
            print query
            cur.execute(query)
            query = "SELECT GID FROM Genre WHERE Name = '" + genre_name + "';"
            cur.execute(query)
            return cur.fetchone()
        else:
            print "Genre already exist in Genre"
            return None

def getLanguages(page_movie):
    list_lang = page_movie.find_class("info")
    list_lang[:] = [a.find('div') for a in list_lang if 'Language' in a.find('h5').text_content()]
    list_lang[:] = list_lang[0].findall('a')
    list_lang[:] = [[a.get('href')[10:], a.text_content()] for a in list_lang]
    return list_lang

def insertLanguage(list_lang):
    lang_id = list_lang[0]
    lang_name = list_lang[1]
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "SELECT * FROM Language WHERE Name = '" + lang_name + "';"
        cur.execute(query)

        if cur.fetchone() is not None:
            query = "INSERT INTO " + tablePrefix + "_Language(LAID, Name) VALUES("\
                    + "'" + lang_id             + "', "\
                    + "'" + lang_name         + "'"\
                    + ")";\
            print query
            cur.execute(query)
        else:
            print "Language already exist in Language"

def getCountry(page_movie):
    list_country = page_movie.find_class("info")
    list_country[:] = [a.find('div') for a in list_country if 'Country' in a.find('h5').text_content()]
    list_country[:] = list_country[0].findall('a')
    list_country[:] = [[a.get('href')[9:], a.text_content()] for a in list_country]
    return list_country

def insertCountry(country):

    country_id = country[0]
    country_name = country[1]

    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "SELECT * FROM Country where CID='" + country_id + "';"

        if cur.fetchone is not None:
            query = "INSERT INTO " + tablePrefix + "_Country(CID, Name) VALUES("\
                    + "'" + country_id             + "', "\
                    + "'" + country_name         + "'"\
                    + ")";\
            print query
            cur.execute(query)
        else:
            print "Country already exist in Country"

def getLocations(movie_id):

    locationPage = "http://www.imdb.com/title/"+ movie_id + "/locations"
    list_locations = lxml.html.document_fromstring(requests.get(locationPage).content).get_element_by_id('filming_locations_content').find_class('sodavote')
    list_locations[:] = [location.find('dt').find('a').text_content() for location in list_locations if location.find('dt').find('a') is not None]

    return list_locations

def insertLocation(location):

    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "SELECT * FROM Location WHERE Name = '" + location + "';"
        cur.execute(query)

        if cur.fetchone() is not None:
            query = "INSERT INTO " + tablePrefix + "_Location(Name) VALUES("\
                    + "'" + location         + "'"\
                    + ")";\
            print query
            cur.execute(query)
            query = "SELECT LID FROM Location WHERE Name = '" + location + "';"
            cur.execute(query)
            return cur.fetchone()
        else:
            print "Location already exist in Location"
            return None

def getDirector(page_movie):
    director = page_movie.get_element_by_id('director-info')
    if director is not None:
        dir_a = director.find('div').find('a')
        print dir_a.get('href')[6:-1], dir_a.text_content()
    else:
        print "NOPE"
    return (dir_a.get('href')[6:-1], dir_a.text_content())

def insertMDirector(movie_id, director):
    insertPerson(director[0])
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Director(MID, PID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + director[0]         + "'"\
                + ")";\
        print query
        cur.execute(query)

def insertMCast(movie_id, actor_id):
    insertPerson(actor_id)
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Cast(MID, PID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + actor_id         + "'"\
                + ")";\
        print query
        cur.execute(query)

def insertMGenre(movie_id, genre_id):
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Genre(MID, GID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + genre_id         + "'"\
                + ")";\
        print query
        cur.execute(query)

def insertMLang(movie_id, lang_id):
    insertLanguage(lang_id)
    lang_id = lang_id[0]
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Language(MID, LAID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + lang_id         + "'"\
                + ")";\
        print query
        cur.execute(query)

def insertMCountry(movie_id, country_id):
    insertCountry(country_id)
    country_id = country_id[0]
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Country(MID, CID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + country_id         + "'"\
                + ")";\
        print query
        cur.execute(query)

def insertMLocation(movie_id, location_id):
    con = db.connect('localhost', 'root', 'root', 'imdb');
    with con:
        cur = con.cursor()
        query = "INSERT INTO " + tablePrefix + "_M_Location(MID, LID) VALUES("\
                + "'" + movie_id             + "', "\
                + "'" + location_id         + "'"\
                + ")";\
        print query
        cur.execute(query)

def crawlIMDB(nextPage, tablePrefix, pageCount = 5):
    for i in range(pageCount):
        page_top_movies = lxml.html.document_fromstring(requests.get(nextPage).content)
        nextPage = "http://www.imdb.com" + str(page_top_movies.find_class("pagination")[0].findall('a')[-1].get('href'))
        list_top_movies = page_top_movies.find_class("results")[0].findall("tr")
        list_top_movies[:] = [movie.findall("td")[2].find("a").get("href")[7:-1] for movie in list_top_movies if len(movie.findall("td"))>2]

        for movie_id in list_top_movies:
            movie = getMovie(movie_id)
            insertMovie(movie_id, movie)
            page_movie = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + movie_id + "/combined").content)

            list_actors = page_movie.find_class("cast")[0].findall("tr")
            list_actors[:] = [actor.findall("td")[1].find("a").get("href")[6:15] for actor in list_actors if len(actor.findall("td"))>1]
            for actor_id in list_actors:
                insertMCast(movie_id, actor_id)

            list_genres = getGenres(page_movie)
            for genre in list_genres:
                genre_id = insertGenre(genre);
                if genre_id is not None:
                    insertMGenre(movie_id, str(genre_id[0]))

            list_lang = getLanguages(page_movie)
            if(len(list_lang)) > 1:
                print "Multilingual movie entered"
                for x in list_lang:
                    print x
            insertMLang(movie_id, list_lang[0])

            list_country = getCountry(page_movie)
            if(len(list_country)) > 1:
                print "Multinational movie entered"
                for x in list_lang:
                    print x
            insertMCountry(movie_id, list_country[0])

            list_locations = getLocations(movie_id)
            if list_locations is not None:
                for location in list_locations:
                    location_id = insertLocation(location)
                    if location_id is not None:
                        insertMLocation(movie_id, str(location_id[0]))

            director = getDirector(page_movie)
            insertMDirector(movie_id, director)

def startCrawlIMDB():
    crawlParam = open("setup.txt")
    pageLink = crawlParam.readline().strip()
    tablePrefix = crawlParam.readline().strip()
    crawlIMDB(pageLink, tablePrefix)

if __name__ == "__main__":
    startCrawlIMDB()
