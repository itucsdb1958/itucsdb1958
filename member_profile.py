# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from forms import *
import psycopg2 as db
import os
import json
import datetime
member_profile = Blueprint(name='member_profile',
						   import_name=__name__, template_folder='templates')


class Person(object):
	def __init__(self, result=None):
		if(result != None):
			self.name = result[1]
			self.age = result[2]
			self.phone = result[3]
			self.cv = result[4]
			self.email = result[5]
			self._class = result[6]
			self.auth_type = result[7]
			self.status = result[8]
			self.team_id = result[9]
			self.subteam_id = result[10]
			self.major_id = result[11]
			self._get_team(self.team_id)
			self._get_subteam(self.subteam_id)
			self._get_major(self.major_id)

	def _get_team(self, id):
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = "select name from team where id={}".format(id)
			cursor.execute(query)
			result = cursor.fetchone()
			if(result != None and len(result) == 1):
				self.team = result[0]
		except Exception as e:
			print(e)
		finally:
			connection.close()

	def _get_subteam(self, id):
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = "select name from subteam where id={}".format(id)
			cursor.execute(query)
			result = cursor.fetchone()
			if(result != None and len(result) == 1):
				self.subteam = result[0]
		except Exception as e:
			print(e)
		finally:
			connection.close()

	def _get_major(self, id):
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			query = "select name from major where id={}".format(id)
			cursor.execute(query)
			result = cursor.fetchone()
			if(result != None and len(result) == 1):
				self.major = result[0]
		except Exception as e:
			print(e)
		finally:
			connection.close()


class Member(Person):
	def __init__(self, member_result, person_result):
		if(member_result != None and person_result != None):
			Person.__init__(self, person_result)
			self.role = member_result[1]
			self.entry = member_result[2]
			self.active = member_result[3]
			self.picture = member_result[4]
			self.address = member_result[5]
			self.person_id = member_result[6]
		else:
			return None

	def toJSON(self):
		return json.dumps(self, default=self.jsonify,
						  sort_keys=True, indent=4)

	def jsonify(self, value):
		if isinstance(value, datetime.date):
			return dict(year=value.year, month=value.month, day=value.day)
		else:
			return value.__dict__


@member_profile.route("/profile")
def member_profile_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		member = Member(None, None)
		member_id = session.get('member_id')
		get_member = "SELECT * FROM MEMBER WHERE ID = {}".format(member_id)
		try:
			connection = db.connect(os.getenv("DATABASE_URL"))
			cursor = connection.cursor()
			cursor.execute(get_member)
			member_result = cursor.fetchone()
			if (member_result != None and len(member_result) >= 0):
				get_person = "SELECT * from person where id = {}".format(
					member_result[6])
				cursor.execute(get_person)
				person_result = cursor.fetchone()
				if (person_result != None and len(person_result) >= 0):
					member = Member(member_result, person_result)
					session['member'] = json.loads(member.toJSON())
					return render_template('member_profile_page.html', member=member)
		except db.DatabaseError:
			connection.rollback()
			flash('There was a problem retrieving Member page.', 'danger')
		finally:
			connection.close()
		if(member == None):
			flash("There was a problem retrieving Member page.", "danger")
			return redirect(url_for('home.home_page'))
		return render_template('member_profile_page.html', member=None)