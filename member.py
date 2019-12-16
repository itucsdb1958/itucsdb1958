# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
from forms import AddMemberForm
from forms import AddEquipmentForm
from forms import AddScheduleForm
from queries import select, insert

member = Blueprint(name='member', import_name=__name__,
				   template_folder='templates')


@member.route("/member/add/member", methods=['GET', 'POST'])
def member_add_member_page():
	if(session['auth_type'] != "Team leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	team_id = select(
		"team.id", "team join person on team.id=person.team_id join member on member.person_id=person.id", "person.id={}".format(session['member_id']))[0]
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
	form = AddMemberForm()
	form.subteam.choices = subteams
	if (request.method == 'POST' and form.submit_add_member.data or form.validate()):
		name = form.name.data
		age = form.age.data
		phone = form.phone.data
		mail = form.mail.data
		subteam = form.subteam.data
		clas = form.clas.data
		status = form.status.data
		major = form.major.data
		username = form.username.data
		major_id = select("id","major","code='{}'".format(major))[0]
		insert("person", "NAME, AGE, PHONE, CV, EMAIL, CLASS, AUTH_TYPE, STATUS, TEAM_ID, SUBTEAM_ID, MAJOR_ID",
			   "'{}','{}','{}','-1','{}',{},1,{},{},{},{}".format(
				   name,age,phone,mail,clas,status,team_id,subteam,major_id
			   ))
		person_id = select("id","person","name='{}'".format(name))[0]
		insert("member","ROLE, ENTRYDATE, ACTIVE, PICTURE, ADDRESS, PERSON_ID",
				"'Uye',CURRENT_DATE,true,'-1','Address',{}".format(person_id))
		member_id = select("id","member","person_id={}".format(person_id))[0]
		insert("users","username,password,member_id","'{}',crypt('1234',gen_salt('bf')),{}".format(username,member_id))
		return redirect(url_for("member.member_add_member_page"))
	return render_template("member_add_member_page.html", form=form)


@member.route("/member/add/equipment", methods=['GET', 'POST'])
def member_add_equipment_page():
	auth = session.get('auth_type')

	if(auth != "Team leader" and auth != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	#team_id = select(
	#	"team.id", "team join person on team.id=person.team_id join member on member.person_id=person.id", "person.id={}".format(session['member_id']))
	team_id = session.get("team_id")
	print("Teamid",team_id)
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
	form = AddEquipmentForm()
	form.subteam.choices=subteams
	if (request.method == 'POST' and form.submit_add_equipment.data or form.validate()):
		name = form.name.data
		link = form.link.data
		purchasedate = form.purchasedate.data
		available = form.available.data
		subteam_id = form.subteam.data
		insert("equipment","NAME, LINK, PURCHASEDATE, AVAILABLE, PICTURE, TEAM_ID, SUBTEAM_ID",
				"'{}','{}','{}','{}','-1','{}','{}'".format(
				   name,link,purchasedate,available,team_id,subteam_id
			   ))
	
		#return redirect(url_for("member.member_add_equipment_page"))
	return render_template("member_add_equipment_page.html", form=form)


@member.route("/member/add/schedule", methods=['GET', 'POST'])
def member_add_schedule_page():
	if(session['auth_type'] != "Team leader" or session['auth_type'] != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	
	form = AddScheduleForm()
	if (request.method == 'POST' and form.submit_add_equipment.data or form.validate()):
		name = form.name.data
		deadline = form.deadline.data
		done = form.done.data
		description = form.description.data
		budget = form.budget.data
				
		insert("schedule","NAME, DEADLINE, DONE, DESCRIPTION, BUDGET, MEMBER_ID",
				"'{}','{}','{}','{}','{}','1'".format(
				   name,deadline,done,description,budget
			   ))
	
		return redirect(url_for("member.member_add_schedule_page"))
	return render_template("member_add_schedule_page.html", form=form)

