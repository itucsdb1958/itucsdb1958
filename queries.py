from flask import flash
import psycopg2 as db
import os


def select(columns,table,where=None):
	if (where != None):
		query = """select {} from {} where {}""".format(columns,table,where)
	else:
		query = """select {} from {}""".format(columns,table)
	return run(query)

def update(table,columns,where):
	query = """update {} set {} where {}""".format(table,columns,where)
	run(query)

def delete(table,where):
	query ="""delete from {} where {}""".format(table,where)
	run(query)

def run(query):
	connection = None
	try:
		connection = db.connect(os.getenv("DATABASE_URL"))
		cursor = connection.cursor()
		cursor.execute(query)
		result = cursor.fetchall()
		resLen = len(result)
	except db.DatabaseError as dberror:
		if connection != None:
			connection.rollback()
		result = dberror
		resLen = 1
		flash('Query unsuccessful.', 'danger')
	finally:
		if connection != None:
			connection.commit()
			connection.close()
		return result