#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'root', 'imdb');

    cur = con.cursor()

    cur.execute("DROP TABLE M_Location;")
    cur.execute("DROP TABLE M_Country;")
    cur.execute("DROP TABLE M_Language;")
    cur.execute("DROP TABLE M_Genre;")
    cur.execute("DROP TABLE M_Cast;")
    cur.execute("DROP TABLE M_Director;")
    cur.execute("DROP TABLE M_Producer;")
    cur.execute("DROP TABLE Location;")
    cur.execute("DROP TABLE Country;")
    cur.execute("DROP TABLE Language;")
    cur.execute("DROP TABLE Genre;")
    cur.execute("DROP TABLE Person;")
    cur.execute("DROP TABLE Movie;")

    print "Tables dropped"

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()
