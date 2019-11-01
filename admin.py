from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db
import os
from forms import SQLForm
sqlpage = Blueprint(name='sqlpage', import_name=__name__)

@sqlpage.route("/admin_sql", methods=['GET', 'POST'])
def sql_page():
	if session.get('member_id') != 'admin':
		flash("Authorization error",'danger')
		return redirect(url_for('home.home_page'))
	else:
		form = SQLForm()
		if form.validate_on_submit():
			query = form.query.data
			print("Running")
			print(query)
			result = None
			resLen = 0
			try:
				connection = db.connect(os.getenv("DATABASE_URL"))
				cursor = connection.cursor()
				cursor.execute(query)
				result = cursor.fetchall()
				resLen = len(result)
			except db.DatabaseError as dberror:
				connection.rollback()
				result = dberror
				resLen = 1
				flash('Query unsuccessful.', 'danger')
			finally:
				connection.close()
				return render_template('sql_page.html', form=form,queryResult=result,resultLen=resLen)
		return render_template('sql_page.html',form=form,error=error,queryResult=None,resultLen=0)
