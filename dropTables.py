# #####################################################
# Name          : NEVIN VALSARAJ
# Roll No       : 12CS10032
# Assignment    : DBMS Lab (cs43002) - Assignment 3
# Date          : 1 FEB 2105
# #####################################################

#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'root', 'imdb');

    cur = con.cursor()

    cur.execute("DROP TABLE M_Location, M_Country, M_Language, M_Genre, M_Cast, M_Director, M_Producer, Location, Country, Language, Genre, Person, Movie")
    print "Tables dropped"

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()
