# -*- coding: utf-8 -*-
import math
import os
import time

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

from forms import (AddCompetitionForm, AddMemberForm, AddSponsorForm,
                   UploadImageForm)
from queries import insert, select, update

member = Blueprint(name='member', import_name=__name__,
				   template_folder='templates')


@member.route("/member/add/member", methods=['GET', 'POST'])
def member_add_member_page():
	if(session.get('auth_type') != "Team leader"):
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
		major_id = select("id", "major", "code='{}'".format(major))[0]
		insert("person", "NAME, AGE, PHONE, CV, EMAIL, CLASS, AUTH_TYPE, STATUS, TEAM_ID, SUBTEAM_ID, MAJOR_ID",
			   "'{}','{}','{}','-1','{}',{},1,{},{},{},{}".format(
				   name, age, phone, mail, clas, status, team_id, subteam, major_id
			   ))
		person_id = select("id", "person", "name='{}'".format(name))[0]
		insert("member", "ROLE, ENTRYDATE, ACTIVE, PICTURE, ADDRESS, PERSON_ID",
			   "'Uye',CURRENT_DATE,true,'-1','Address',{}".format(person_id))
		member_id = select("id", "member", "person_id={}".format(person_id))[0]
		insert("users", "username,password,member_id",
			   "'{}',crypt('1234',gen_salt('bf')),{}".format(username, member_id))
		return redirect(url_for("member.member_add_member_page"))
	return render_template("member_add_member_page.html", form=form)


@member.route("/member/add/competition", methods=['GET', 'POST'])
def member_add_competition_page():
	print("here")
	auth = session.get('auth_type')
	if(auth != "Team leader" and auth != "Subteam leader" and auth != "Member"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	form = AddCompetitionForm()
	if (request.method == 'POST' and form.submit_add_competition.data or form.validate()):
		name = form.name.data
		description = form.description.data
		reward = form.reward.data
		date = form.date.data
		country = form.country.data

		insert("competition", "name,date,country,description,reward",
			   "'{}','{}','{}','{}','{}'".format(name, date, country, description, reward))

	return render_template("member_add_competition_page.html", form=form)


@member.route("/member/add/sponsor", methods=['GET', 'POST'])
def member_add_sponsor_page():
	auth = session.get('auth_type')
	sponsortypechoices = select(
		"sponsortype.id,sponsortype.name", "sponsortype")
	form = AddSponsorForm()
	form.typ.choices = sponsortypechoices
	if(auth != "Team leader" and auth != "Subteam leader" and auth != "Member"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	if (request.method == 'POST' and form.submit_add_sponsor.data or form.validate()):
		name = form.name.data
		description = form.description.data
		address = form.address.data
		field = form.field.data
		country = form.country.data
		type_id = form.typ.data
		insert("sponsor", "name,description,field,country,logo,address,type_id",
			   "'{}','{}','{}','{}','-1','{}',{}".format(name, description, field, country, address, type_id))
		return redirect(url_for("member.member_add_sponsor_page"))
	return render_template("member_add_sponsor_page.html", form=form)


@member.route("/member/edit/sponsor/<sponsor_id>", methods=['GET', 'POST'])
def member_edit_sponsor_page(sponsor_id):
	auth = session.get('auth_type')
	sponsortypechoices = select(
		"sponsortype.id,sponsortype.name", "sponsortype")
	form = AddSponsorForm()
	form.typ.choices = sponsortypechoices
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/sponsors')
	if(auth != "Team leader" and auth != "Subteam leader" and auth != "Member"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	if (request.method == 'POST' and form.submit_add_sponsor.data or form.validate()):
		name = form.name.data
		description = form.description.data
		address = form.address.data
		field = form.field.data
		country = form.country.data
		type_id = form.typ.data
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(sponsor_id, date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(sponsor_id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(sponsor_id)):
					print("deleting",im)
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash("Please upload a file in JPG format", 'danger')
		print(name,description,address,field,country,type_id)
		update("sponsor", "name='{}',description='{}',field='{}',country='{}',logo='-1',address='{}',type_id={}".format(
			name, description, field, country, address, type_id), where="id={}".format(sponsor_id))
		return redirect(url_for("visitor.visitor_sponsors_page"))
	else:
		img_name = None
		for img in os.listdir(imageFolderPath):
			if(sponsor_id in img[0:len(sponsor_id)] and (img[len(sponsor_id)] == '_' or img[len(sponsor_id)] == '.')):
				img_name = img
		result = select("sponsor.name,description,field,country,logo,address,type_id",
						"sponsor join sponsortype on sponsor.type_id=sponsortype.id", "sponsor.id={}".format(sponsor_id))
		print(result)
		form.name.data = result[0]
		form.description.data = result[1]
		form.field.data = result[2]
		form.country.data = result[3]
		form.address.data = result[5]
		form.typ.data = sponsortypechoices[result[6]]
		return render_template("member_edit_sponsor_page.html", form=form, uploadImg=imageForm,result=result,imgName=img_name)