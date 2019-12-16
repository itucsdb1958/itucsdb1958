# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
import os
import time
import math
from forms import AddMemberForm,AddTutorialForm,EditTutorialForm,UploadImageForm
from queries import select, insert, update, delete
from werkzeug.utils import secure_filename
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
		return redirect(url_for("visitor.visitor_tutorials_page"))
	return render_template("member_add_tutorial_page.html",form=form)

@member.route("/member/tutorial/edit/<id>", methods=['GET', 'POST'])
def member_edit_tutorial_page(id):
	form = EditTutorialForm()
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/tutorial')

	if (request.method == 'POST' and form.submit_edit_tutorial.data or form.validate()):
		name = form.name.data
		area = form.area.data
		description = form.description.data
		link = form.link.data
		isvideo = form.isvideo.data
		member_id = session.get('member_id')
		image = imageForm.image.data

		if(image):
			extension=image.filename.split('.')[1]
			current_date = time.gmtime()
			filename = secure_filename(
				"{}_{}.{}".format(id, current_date[0:6],extension))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash('Please upload a file in JPG format', "danger")

		update("tutorial", "name='{}', area='{}', description='{}', picture='{}',link='{}', isvideo={}".format(
			name, area, description, filename,link, isvideo), where="id={}".format(id))
		return redirect(url_for('visitor.visitor_tutorials_page'))
	else:
		if(session.get('auth_type') == 'Member' or session.get('auth_type') == 'Team leader' or session.get('auth_type') == 'Subteam leader'):
			result = select(columns="tutorial.name,tutorial.area,tutorial.description,tutorial.link,tutorial.isvideo,tutorial.picture,tutorial.member_id",
						table="tutorial",
						where="tutorial.id={}".format(id))
			form.name.data = result[0]
			form.area.data = result[1]
			form.description.data = result[2]
			form.link.data = result[3]
			form.isvideo.data = result[4]
			img_name = result[5]
			
		else:
			flash('Not an authorized person', 'danger')
			return redirect(url_for('visitor.visitor_tutorials_page'))
		
		return render_template('member_edit_tutorial_page.html', form=form, result=result, uploadImg=imageForm)
	return render_template('member_edit_tutorial_page.html', form=form, result=result, uploadImg=imageForm,imgName=img_name)

@member.route("/member/delete/tutorial/<tutorial_id>",methods=['GET','POST'])
def member_delete_tutorial_page(tutorial_id):
	auth = session.get('auth_type')
	member_id = session.get('member_id')

	if(auth != "Team leader" and auth != "admin" and auth != "Subteam leader" and auth != "Member"):
		flash("Not an authorized person")
		return redirect(url_for("visitor.visitor_tutorials_page"))
	if( member_id == select("member_id","tutorial","id={}".format(tutorial_id))[0] ):
		delete(table="tutorial",where="id={}".format(tutorial_id))
	else:
		flash("Not an authorized person")
		return redirect(url_for("visitor.visitor_tutorials_page"))
	return redirect(url_for("visitor.visitor_tutorials_page"))