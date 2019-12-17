# -*- coding: utf-8 -*-
import os

import psycopg2 as db
from flask import flash

def insert(table,columns,values):
    query = """insert into {} ({}) values({})""".format(table,columns,values)
    run(query)

def select(columns, table, where=None):
    if (where != None):
        query = """select {} from {} where {}""".format(columns, table, where)
    else:
        query = """select {} from {}""".format(columns, table)
    return run(query)


def update(table, columns, where):
    query = """update {} set {} where {}""".format(table, columns, where)
    run(query)


def delete(table, where):
    query = """delete from {} where {}""".format(table, where)
    run(query)


def run(query):
    connection = None
    cursor = None
    result = None
    print(query)
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(query)
        if(not 'drop' in query and not 'update' in query and not 'delete' in query and not 'insert' in query):
            result = cursor.fetchall()
    except db.DatabaseError as dberror:
        if connection != None:
            connection.rollback()
        result = dberror
        print("Error",result)
        flash(result.message, 'danger')
    finally:
        if connection != None:
            connection.commit()
            connection.close()
        if cursor != None:
            cursor.close()
        #if(type(result) == list and len(result) == 1):
        #    return result[0]
        print(result)
        return result
