# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
from forms import AddMemberForm,AddTutorialForm,EditTutorialForm
from queries import select, insert, update

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

@member.route("/member/add/tutorial", methods=['GET', 'POST'])
def member_add_tutorial_page():
	if(session['auth_type'] != "Team leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	
	form = AddTutorialForm()
	#imageForm 
	if (request.method == 'POST' and form.submit_add_tutorial.data or form.validate()):
		name = form.name.data
		area = form.area.data
		description = form.description.data
		link = form.link.data
		isvideo = form.isvideo.data
		member_id = session.get('member_id')

		insert("tutorial" , "NAME, AREA, DESCRIPTION, LINK, PICTURE, ISVIDEO, MEMBER_ID",
		 "'{}','{}','{}','{}','avatar',{},{}".format(name, area, description, link, isvideo, member_id))
		return redirect(url_for("member.member_add_tutorial_page"))
	return render_template("member_add_tutorial_page.html",form=form)

@member.route("/member/tutorials/edit/<id>", methods=['GET', 'POST'])
def member_edit_tutorial_page(id):
	form = EditTutorialForm()

	if (request.method == 'POST' and form.submit_edit_tutorial.data or form.validate()):
		name = form.name.data
		area = form.area.data
		description = form.description.data
		link = form.link.data
		isvideo = form.isvideo.data
		member_id = session.get('member_id')

		update("tutorial", "name='{}', area='{}', description='{}', link='{}', isvideo={}".format(
			name, area, description, link, isvideo), where="id={}".format(id))
		return redirect(url_for('member.member_edit_tutorial_page', id=id))
	else:
		if(session.get('auth_type') == 'Member' or session.get('auth_type') == 'Team leader' or session.get('auth_type') == 'Subteam leader'):
			result = select(columns="tutorial.name,tutorial.area,tutorial.description,tutorial.link,tutorial.isvideo,tutorial.member_id",
						table="tutorial",
						where="tutorial.id={}".format(id))
		else:
			flash('No member privileges...', 'danger')
			return redirect(url_for('home.home_page'))
		
		return render_template('member_edit_tutorial_page.html', form=form, result=result)
	return render_template('member_edit_tutorial_page.html', form=form, result=result)