# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
from forms import LoginForm
import psycopg2 as db
from Crypto.Hash import SHA256
from dbinit import DATABASE_URL


login = Blueprint(name='login', import_name=__name__,template_folder='templates')
logout = Blueprint(name='logout',import_name=__name__,template_folder='templates')

@login.route("/login", methods=['GET', 'POST'])
def login_page():
	if session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			username = form.username.data
			password = form.password.data
			try:
				connection = db.connect(DATABASE_URL)
				cursor = connection.cursor()
				statement = """SELECT * FROM USERS WHERE USERNAME = '%s' AND PASSWORD = crypt('%s',PASSWORD)
						""" % (username,password)
				cursor.execute(statement)
				result = cursor.fetchone()
				if(result is not None and len(result) >= 1):
					flash('You have been logged in!', 'success')
					session['logged_in'] = True
					session['id'] = username
					session['member_id'] = result[2]
					#session['team'] = result[3]
					return redirect(url_for('home.home_page'))
				else:
					flash(
						'Login Unsuccessful. Please check username and password', 'danger')
			except db.DatabaseError:
				connection.rollback()
				flash('Login Unsuccessful. Please check username and password', 'danger')
			finally:
				connection.close()
		return render_template('login_page.html', form=form)

@logout.route("/logout")
def logout_page():
	if session.get('logged_in'):
		try:
			session.pop('username', None)
			session['member_id'] = 0
			session['logged_in'] = False
			flash('You have been successfully logged out.','success')
		except:
			flash('Logging out is not completed.')
	return redirect(url_for('home.home_page'))
