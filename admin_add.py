# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import Blueprint, redirect, render_template, url_for, session, flash, request

from forms import AddTeamForm,AddTeamLeaderForm
from queries import insert,select

admin_add = Blueprint(name='admin_add', import_name=__name__)


@admin_add.route("/admin/add/team", methods=['GET', 'POST'])
def admin_add_team_page():
	if(session.get('auth_type') != 'admin'):
		flash('No admin privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		form = AddTeamForm()
		if (request.method == 'POST' and form.submit_add_team.data or form.validate()):
			name = form.name.data
			email = form.mail.data
			address = form.address.data
			year = form.year.data
			insert("team", "name,num_members,found_year,email,adress,logo,competition_id",
				   "'{}',0,'{}','{}','{}','-1',NULL".format(name, year, email, address))
			return redirect(url_for('admin_add.admin_add_team_page'))
		return render_template('admin_add_team_page.html', imgName=None, form=form)


@admin_add.route("/admin/add/team_leader", methods=['GET', 'POST'])
def admin_add_team_leader_page():
	if(session.get('auth_type') != "admin"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	form = AddTeamLeaderForm()
	teams = select("id,name","team")
	form.team.choices = teams
	majors = select("id,name","major")
	form.major.choices=majors
	if (request.method == 'POST' and form.submit_add_team_leader.data or form.validate()):
		name = form.name.data
		age = form.age.data
		phone = form.phone.data
		mail = form.mail.data
		clas = form.clas.data
		status = form.status.data
		username = form.username.data
		team_id = form.team.data
		major = form.major.data
		insert("person", "NAME, AGE, PHONE, CV, EMAIL, CLASS, AUTH_TYPE, STATUS, TEAM_ID, SUBTEAM_ID, MAJOR_ID",
			   "'{}','{}','{}','-1','{}',{},3,{},{},{},{}".format(
				   name, age, phone, mail, clas, status, team_id, 1, major
			   ))
		person_id = select("id", "person", "name='{}'".format(name))[0]
		insert("member", "ROLE, ENTRYDATE, ACTIVE, PICTURE, ADDRESS, PERSON_ID",
			   "'Uye',CURRENT_DATE,true,'-1','Address',{}".format(person_id))
		member_id = select("id", "member", "person_id={}".format(person_id))[0]
		insert("users", "username,password,member_id",
			   "'{}',crypt('1234',gen_salt('bf')),{}".format(username, member_id))
		return redirect(url_for("admin_add.admin_add_team_leader_page"))
	return render_template("admin_add_team_leader_page.html", form=form)
