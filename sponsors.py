# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db
import os 

sponsors= Blueprint(name='sponsors', import_name=__name__)

@sponsors.route("/sponsors")
def sponsors_page():
    connection = None
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        query = "select name,description,field,country,logo,address from sponsor order by sponsor.name asc"
        cursor.execute(query)
        result = cursor.fetchall()
        resLen = len(result)
    except db.DatabaseError as dberror:
        connection.rollback()
        result = dberror
        resLen = 1
        flash('Query unsuccessful.', 'danger')
    finally:
        if connection != None:
            connection.close()

    return render_template('sponsors_page.html',sponsors=result,resLen=resLen)
