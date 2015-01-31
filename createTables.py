#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'root', 'root', 'imdb');

    cur = con.cursor()
    query = ""

    with file('imdb_createschema.sql') as sql:
        for line in sql:
            query += line.strip()
            if(len(query) > 1 and query[-1] == ';'):
                print query
                cur.execute(query)
                query = ""

    print "Tables created"

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    if con:
        con.close()
