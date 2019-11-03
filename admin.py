from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
import os
from HelperClasses import Competition
from forms import SQLForm
admin = Blueprint(name='admin', import_name=__name__)


@admin.route("/admin")
def admin_page():
	if (session.get('member_id') == 'admin'):
		return render_template('admin_page.html')
	else:
		return redirect(url_for('home.home_page'))


@admin.route("/admin/sql", methods=['GET', 'POST'])
def sql_page():
	form = SQLForm()
	if form.validate_on_submit():
		query = form.query.data
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
			return render_template('sql_page.html', form=form, queryResult=result, resultLen=resLen)
	return render_template('sql_page.html', form=form, queryResult=None, resultLen=0)


@admin.route("/admin/competitions")
def admin_competitions_page():
	if(session.get('member_id') != 'admin'):
		flash('No admin privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = "select * from competition order by competition.name asc"
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
			return render_template('admin_competitions_page.html', competitions=result, length=resLen)


@admin.route("/admin/teams")
def admin_teams_page():
	if(session.get('member_id') != 'admin'):
		flash('No admin privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = """select team.name,competition.name,team.email,team.adress \
					from team join competition \
					on team.competition_id=competition.id\
					order by team.name desc"""
			cursor.execute(query)
			result = cursor.fetchall()
			resLen = len(result)
		except db.DatabaseError as dberror:
			connection.rollback()
			result = dberror
			resLen = 1
			print(dberror)
			flash('Query unsuccessful.', 'danger')
		finally:
			connection.close()
			return render_template('admin_teams_page.html', team=result, length=resLen)

@admin.route("/admin/members")
def admin_members_page():
	if(session.get('member_id') != 'admin'):
		flash('No admin privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = """select person.name,person.email,auth_type.name,team.name \
						from person join team \
						on person.team_id=team.id \
						join auth_type on person.auth_type=auth_type.id \
						order by team.name asc, auth_type.name desc"""
			cursor.execute(query)
			result = cursor.fetchall()
			resLen = len(result)
		except db.DatabaseError as dberror:
			connection.rollback()
			result = dberror
			resLen = 1
			print(dberror)
			flash('Query unsuccessful.', 'danger')
		finally:
			connection.close()
			return render_template('admin_members_page.html', members=result, length=resLen)