# -*- coding: utf-8 -*-
import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

from forms import (EditCompetitionForm, EditMemberForm, EditTeamForm, SQLForm,
				   UploadCVForm, UploadImageForm)
from member_profile import Member
from queries import run, select, update

admin_edit = Blueprint(name='admin_edit', import_name=__name__)


@admin_edit.route("/admin/competitions/edit/<id>", methods=['GET', 'POST'])
def admin_edit_competition_page(id):
	form = EditCompetitionForm()
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/competitions')

	if (request.method == 'POST' and form.submit_competition.data or form.validate()):
		name = form.name.data
		date = form.date.data
		country = form.country.data
		description = form.description.data
		reward = form.reward.data
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			current_date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(id, current_date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash('Please upload a file in JPG format', "danger")
		print("Before update: ", date)
		update("competition", "name='{}', date=DATE('{}'), country='{}', description='{}', reward='{}'".format(
			name, date, country, description, reward), "id={}".format(id))
		return redirect(url_for('admin_edit.admin_edit_competition_page', id=id))
	else:
		if(session.get('auth_type') != 'Team leader'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))
		result = select('id,name,date,country,description,reward',
						'competition', 'id={}'.format(id))[0]
		img_name = None
		for img in os.listdir(imageFolderPath):
			if(id in img[0:len(id)] and (img[len(id)] == '_' or img[len(id)] == '.')):
				img_name = img
		form.description.data = result[4]
		return render_template('admin_edit_competition_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)
	return render_template('admin_edit_competition_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)


@admin_edit.route("/admin/teams/edit/<id>", methods=['GET', 'POST'])
def admin_edit_team_page(id):
	auth = session.get('auth_type')
	if(auth!='admin' and (auth!='Team leader' and id!=session.get('team_id'))):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))
	form = EditTeamForm()
	competitions = select("id,name", "competition")
	form.competition.choices = competitions
	imgForm = UploadImageForm()
	imgFolder = os.path.join(os.getcwd(), 'static/images/team')
	if (request.method == 'POST' and form.submit_team.data or form.validate()):
		name = form.name.data
		members = form.memberCtr.data
		year = form.year.data
		email = form.email.data
		address = form.address.data
		competition = form.competition.data
		image = imgForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename or '.png' in image.filename):
			date = time.gmtime()
			extension = image.filename.split('.')[1]
			filename = secure_filename(
				"{}_{}.{}".format(id, date[0:6], extension))
			filePath = os.path.join(imgFolder, filename)
			images = os.listdir(imgFolder)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imgFolder, im))
			image.save(filePath)
			update("team","logo='{}'".format(filename),"id={}".format(id))
		elif(image):
			flash("Please upload a file in JPG format", 'danger')
		
		update("team", "name='{}', num_members={}, found_year='{}', email='{}', adress='{}', competition_id={}".format(
			name, members, year, email, address, competition), where="id={}".format(id))
		return redirect(url_for('admin_edit.admin_edit_team_page', id=id))
	else:
		result = select(columns="team.name,team.num_members,team.found_year,team.email,team.adress,team.logo,competition.id",
						table="team left outer join competition on team.COMPETITION_ID=competition.id",
						where="team.id={}".format(id))
		print("EDIT TEAM RESULT",result)
		form.name.data = result[0]
		form.memberCtr.data = result[1]
		form.year.data = result[2]
		form.email.data = result[3]
		form.address.data = result[4]
		img_name = result[5]
		form.competition.data = result[6]
		return render_template('admin_edit_team_page.html', form=form, result=result, uploadImg=imgForm,imgName=img_name)
	return render_template('admin_edit_team_page.html', form=form, result=result, uploadImg=imgForm,imgName=img_name)


@admin_edit.route("/admin/members/edit/<person_id>", methods=['GET', 'POST'])
def admin_edit_member_page(person_id):
	# TODO:: Alter table to include social accounts links in person database.
	auth = session.get('auth_type')
	if(auth!='admin'):
		flash("No admin",'danger')
		return redirect(url_for("home.home_page"))
	form = EditMemberForm()
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id join person on person.team_id=team.id", "person.id={}".format(person_id))
	form.subteam.choices = subteams
	majors = select("major.id,major.name","major")
	form.major.choices=majors
	auth_types = select("id,name","auth_type")
	form.auth_type.choices=auth_types
	cvForm = UploadCVForm()
	cvPath = None
	cvFolder = os.path.join(os.getcwd(), 'static/cv')
	imgForm = UploadImageForm()
	imgPath = None
	imgFolder = os.path.join(os.getcwd(), 'static/images/person')
	member_id = select("member.id","member join person on person.id=member.person_id",where="person.id={}".format(person_id))[0]
	if form.validate_on_submit():
		team = form.team.data
		subteam = form.subteam.data
		role = form.role.data
		auth_type = form.auth_type.data
		email = form.email.data
		name = form.name.data
		address = form.address.data
		active = form.active.data
		age = form.age.data
		phone = form.phone.data
		clas = form.clas.data
		major = form.major.data
		cv = cvForm.cv.data
		image = imgForm.image.data
		if(cv and '.pdf' in cv.filename):
			date = time.gmtime()
			filename = secure_filename(
				"{}_{}.pdf".format(person_id, date[0:6]))
			cvPath = os.path.join(cvFolder, filename)
			cvs = os.listdir(cvFolder)
			digits = int(math.log(int(person_id), 10))+1
			for c in cvs:
				if(c[digits] == '_' and c[0:digits] == str(person_id)):
					os.remove(os.path.join(cvFolder, c))
			cv.save(cvPath)
			update("person", "cv='{}'".format(
				filename), "id={}".format(person_id))
			session['person_id'] = person_id
			
		elif(cv):
			flash("Upload a PDF file.", 'danger')

		if(image and '.jpg' in image.filename or '.jpeg' in image.filename or '.png' in image.filename):
			date = time.gmtime()
			extension = image.filename.split('.')[1]
			filename = secure_filename(
				"{}_{}.{}".format(person_id, date[0:6], extension))
			imgPath = os.path.join(imgFolder, filename)
			images = os.listdir(imgFolder)
			digits = int(math.log(int(person_id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(person_id)):
					os.remove(os.path.join(imgFolder, im))
			image.save(imgPath)
			update("member", "picture='{}'".format(
				filename), "id={}".format(member_id))
		elif(image):
			flash("Please upload a file in JPG format", 'danger')

		teamID = select(columns="id", table="team",
						where="name='{}'".format(team))[0]
		majorID = select(columns="id", table="major",
						 where="id='{}'".format(major))[0]
		
		update("member", "role='{}', active={}, address='{}'".format(
			role, active, address), where="id={}".format(member_id))

		update("person", "name='{}', age='{}', phone='{}',email='{}', \
					class={}, auth_type={}, team_id={}, subteam_id={}, major_id={}".format(
			name, age, phone, email, clas, auth_type, teamID, subteam, majorID), where="id={}".format(person_id))

		return redirect(url_for('admin_edit.admin_edit_member_page', person_id=person_id, cvPath=person_id))
	else:
		
		result = select("person.name,person.email,team.name,subteam.id,member.role,member.active, \
					member.entrydate,auth_type.id,member.address,person.phone,major.id, \
					person.class,person.age,person.cv,member.picture",
					"person join member on member.person_id=person.id \
					join team on person.team_id=team.id \
					join subteam on person.subteam_id=subteam.id \
					join auth_type on person.auth_type=auth_type.id \
					join major on person.major_id=major.id	",
					"person.id={}".format(person_id))
		form.name.data = result[0]
		form.email.data = result[1]
		form.team.data = result[2]
		form.subteam.data = result[3]
		form.role.data = result[4]
		form.active.data = result[5]
		form.entry.data = result[6]
		form.auth_type.data = result[7]
		form.address.data = result[8]
		form.phone.data = result[9]
		form.major.data = result[10]
		form.clas.data = result[11]
		form.age.data = result[12]
		cvPath = result[13]
		img_name = result[14]

		return render_template('admin_edit_member_page.html', form=form, uploadImg=imgForm, uploadCV=cvForm, cvPath=cvPath, imgName=img_name)


@admin_edit.route("/download", methods=['GET', 'POST'])
def download():
	cvFolder = os.path.join(admin_edit.root_path, "static/cv")
	filename = select("person.cv","person join member on member.person_id=person.id","person.id={}".format(session.get('person_id')))[0]
	return send_from_directory(directory=cvFolder, filename=filename, as_attachment=True, cache_timeout=0)
