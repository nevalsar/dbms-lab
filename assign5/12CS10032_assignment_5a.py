#!/usr/bin/env python

# #######################################################
# Name              : NEVIN VALSARAJ
# Roll No           : 12CS10032
# Assignment        : DBMS Lab (CS43002) - Assignment 5a
# Date              : 3 MAR 2015
# #######################################################

import MySQLdb as db
import networkx


def get_tables():
    table_prefix = "12CS10032_"
    table_name = "M_Cast"
    # connect to database
    con = db.connect('localhost', '12CS10032', 'btech12', '12CS10032')
    with con:
        cur = con.cursor()
        # prepare query statement
        query = "SELECT A.MID, B.MID FROM " + table_prefix + \
            table_name + " AS A JOIN " + table_prefix + table_name +\
            " AS B USING (PID) WHERE A.MID < B.MID GROUP BY A.MID, B.MID;"
        # execute query
        cur.execute(query)
        # return query results
        return cur.fetchall()


def main():
    # get list of connected movies from table of cast
    # 2 movies are connected if they have at least one common cast member
    data = get_tables()
    # generate empty graph
    graph = networkx.Graph()
    # add edges to graph
    for row in data:
        graph.add_edge(row[0], row[1])
    # print (approximation) of size of maximum clique
    # Finding maximum clique is an NP-hard problem.
    print "Maximum clique number : " + str(networkx.graph_clique_number(graph))

if __name__ == '__main__':
    main()
