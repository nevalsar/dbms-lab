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

    cur.execute("DROP TABLE 12CS10032_M_Location, 12CS10032_M_Country, 12CS10032_M_Language, 12CS10032_M_Genre, 12CS10032_M_Cast, 12CS10032_M_Director, 12CS10032_M_Producer, 12CS10032_Movie, 12CS10032_Person, 12CS10032_Genre, 12CS10032_Language, 12CS10032_Country, 12CS10032_Location")
    print "Tables dropped"

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()



