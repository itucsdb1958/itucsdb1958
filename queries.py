# -*- coding: utf-8 -*-
import os

import psycopg2 as db
from flask import flash


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
    result = None
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(query)
        if(not 'drop' in query and not 'update' in query and not 'delete' in query):
            result = cursor.fetchall()
    except db.DatabaseError as dberror:
        if connection != None:
            connection.rollback()
        result = dberror
        flash('Query unsuccessful.', 'danger')
    finally:
        if connection != None:
            connection.commit()
            connection.close()
            cursor.close()
        if(type(result) == list and len(result) == 1):
            return result[0]
        return result
