#!/usr/bin/env python

# #######################################################
# Name              : NEVIN VALSARAJ
# Roll No           : 12CS10032
# Assignment        : DBMS Lab (CS43002) - Assignment 5b
# Date              : 3 MAR 2015
# #######################################################

import MySQLdb as db
import networkx


# Function to get all connected cast members
# Returns all cast members who have done at least one movie together
def get_cast_data():
    table_prefix = "12CS10032_"
    table_name = "M_Cast"
    # connect to database
    con = db.connect('localhost', '12CS10032', 'btech12', '12CS10032')
    with con:
        cur = con.cursor()
        # prepare query statement
        query = "SELECT A.PID, B.PID FROM " + table_prefix + table_name +\
            " AS A JOIN " + table_prefix + table_name + " AS B USING (MID) \
            GROUP BY A.PID, B.PID HAVING A.PID < B.PID ORDER BY A.PID, B.PID;"
        # execute query
        cur.execute(query)
        # return query results
        return cur.fetchall()


# function to drop separation table if it exists
# creates new separation table
def reset_separation_table():
    table_prefix = "12CS10032_"
    table_name = "Separation"
    # donnect to database
    con = db.connect('localhost', '12CS10032', 'btech12', '12CS10032')
    with con:
        cur = con.cursor()
        # drop table if it exists
        query = "DROP TABLE IF EXISTS " + table_prefix + table_name + ";"
        cur.execute(query)
        # create table from schema
        query = "CREATE TABLE " + table_prefix + table_name + \
            "(actor_1 varchar(15), actor_2 varchar(15), separation integer);"
        cur.execute(query)


# function to insert values into separation table
def insert_separation(actor_1, actor_2, separation):
    table_prefix = "12CS10032_"
    table_name = "Separation"
    # set value of string to be entered as the separation into the table
    if separation == 0:
        # use NULL if actor_1 and actor_2 are not connected
        separation_sqlval = "NULL"
    else:
        # convert separation into string to add to sql query
        separation_sqlval = str(separation)
    # connect to database
    con = db.connect('localhost', '12CS10032', 'btech12', '12CS10032')
    with con:
        cur = con.cursor()
        # prepare query statement
        query = "INSERT INTO " + table_prefix + table_name + "(actor_1, \
            actor_2, separation) VALUES('" + actor_1 + "', '" + actor_2 +\
            "', " + separation_sqlval + ");"
        # execute query
        cur.execute(query)


# function to print details of the Separation table
# uses data from Person table to print name of the cast
# Rows are sorted using PID of actor 1 and PID of actor 2, in that order
# (Names of actors are not used to sort - may no be unique)
def print_separation_details():
    table_prefix = "12CS10032_"
    table_name_1 = "Separation"
    table_name_2 = "Person"
    # connect to database
    con = db.connect('localhost', '12CS10032', 'btech12', '12CS10032')
    with con:
        cur = con.cursor()
        # prepare query statement
        query = "select A.actor_1, A.actor_2, B.Name, C.Name, A.separation \
            from " + table_prefix + table_name_2 + " as B join " + \
            table_prefix + table_name_1 + " as A on (A.actor_1 = B.PID) join "\
            + table_prefix + table_name_2 + " as C on (C.PID = A.actor_2) order\
             by A.actor_1, A.actor_2;"
        # execute query
        cur.execute(query)

        # fetch and print rows one by one from query results
        for i in range(cur.rowcount):
            row = cur.fetchone()
            # if connected, print "Yes", if not connected, print "No"
            if row[4] is None:
                print row[0], row[1], "No ", row[2], row[3]
            else:
                print row[0], row[1], "Yes", row[2], row[3]


# main function
def main():
    # get data of all connected actors
    data = get_cast_data()
    # drop and recreate separation table
    reset_separation_table()
    # create empty graph
    graph = networkx.Graph()
    # add edges to graph for each pair of connected actors
    for row in data:
        graph.add_edge(row[0], row[1])

    # iterate through each unique pair of nodes
    for x in graph.nodes_iter():
        for y in graph.nodes_iter():
            if x < y:
                # if the node-pair is connected, insert shortest distance to
                # separation table
                if(networkx.has_path(graph, x, y)):
                    separation = len(networkx.shortest_path(graph, x, y)) - 1
                    insert_separation(x, y, separation)
                    print "insert " + x + ", " + y + ", " + str(separation)
                # else use 0 as separation - will be inserted as NULL in table
                else:
                    insert_separation(x, y, 0)
                    print "insert " + x + ", " + y + ", " + "NULL"
    # print details of separation table
    print_separation_details()
    # print criteria used for sorting
    print """
    Sorted lexicographically using : PID_of_actor_1, PID_of_actor_2
    (Not Names of actors which are not unique.)
    """


if __name__ == '__main__':
    main()
