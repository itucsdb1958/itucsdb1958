import math
import os
import time

from flask import (Blueprint, flash, redirect, render_template, request,
				   session, url_for)
from werkzeug.utils import secure_filename

from forms import *
from queries import select, update

member_edit = Blueprint(name='member_edit', import_name=__name__,
						template_folder='templates')


@member_edit.route("/member/edit/tutorial/<id>", methods=['GET', 'POST'])
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
		filename = select("picture", "tutorial", "id={}".format(id))[0]
		if(image):
			extension = image.filename.split('.')[1]
			current_date = time.gmtime()
			filename = secure_filename(
				"{}_{}.{}".format(id, current_date[0:6], extension))
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
			name, area, description, filename, link, isvideo), where="id={}".format(id))
		return redirect(url_for('visitor.visitor_tutorials_page'))
	else:
		if(session.get('auth_type') == 'Member' or session.get('auth_type') == 'Team leader' or session.get('auth_type') == 'Subteam leader'):
			result = select(columns="tutorial.name,tutorial.area,tutorial.description,tutorial.link,tutorial.isvideo,tutorial.picture,tutorial.member_id",
							table="tutorial",
							where="tutorial.id={}".format(id))
			print("QUERY-", result)
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
	return render_template('member_edit_tutorial_page.html', form=form, result=result, uploadImg=imageForm, imgName=img_name)


@member_edit.route("/member/edit/member/<person_id>", methods=['GET', 'POST'])
def member_edit_member_page(person_id):
	auth = session.get('auth_type')
	if(auth != 'Team leader'):
		flash("Not authorized", 'danger')
		return redirect(url_for("home.home_page"))
	form = EditMemberForm()
	team_id = session.get("team_id")
	print("Teamid", team_id)
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
	current_auth = select("auth_type", "person", "id={}".format(person_id))
	majors = select("id,name","major")
	auths = select("id,name","auth_type")
	form.subteam.choices = subteams
	form.major.choices = majors
	form.auth_type.choices=auths
	form.auth_type.data = current_auth
	if (request.method == 'POST' and form.submit_member.data or form.validate()):
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

		memberID = select(columns="member.id",
						  table="member join person on member.person_id=person.id",
						  where="person.id={}".format(person_id))

		memberID,auth_type = memberID[0],auth_type[0]
		print("Updating...")
		update("member", "role='{}', active={}, address='{}'".format(
			role, active, address), where="id={}".format(memberID))

		update("person", "name='{}', age='{}', phone='{}', email='{}', \
					class={}, auth_type={}, subteam_id={}".format(
			name, age, phone,  email, clas, auth_type, subteam), where="id={}".format(person_id))

		return redirect(url_for('member_edit.member_edit_member_page', person_id=person_id))
	else:
		if(session.get('auth_type') != 'Team leader'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))
		else:
			columns = """person.name,person.email,team.name,subteam.id,\
					member.role,member.active,member.entrydate,auth_type.id, \
					member.address,person.phone,major.id,person.class,person.age,member.id,member.picture"""

			table = """member join person on member.person_id=person.id \
					join major on person.major_id=major.id \
					join team on person.team_id=team.id \
					join subteam on person.subteam_id=subteam.id \
					join auth_type on person.auth_type=auth_type.id"""

			where = "person.id={}".format(person_id)
			result = select(columns, table, where)
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
			form.major.data = result[11]
			form.clas.data = result[12]
			form.age.data = result[13]
			img_name = result[14]
			return render_template('member_edit_member_page.html', form=form, result=result, imgName=img_name)
	return render_template('member_edit_member_page.html', form=form)


@member_edit.route("/member/edit/schedule/<schedule_id>", methods=['GET', 'POST'])
def member_edit_schedule_page(schedule_id):
	auth = session.get('auth_type')
	print(auth)
	if(auth != "Team leader" and auth != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))

	member_id = session.get('member_id')
	form = EditScheduleForm()

	if (request.method == 'POST' and form.submit_edit_schedule.data or form.validate()):
		name = form.name.data
		deadline = form.deadline.data
		done = form.done.data
		description = form.description.data
		budget = form.budget.data

		update("schedule", "name='{}',deadline='{}',done='{}',description='{}',budget='{}', member_id='{}'".format(
			name, deadline, done, description, budget, member_id), where="id={}".format(schedule_id))
		return redirect(url_for("team.team_schedule_page"))
	else:
		result = select("schedule.name,deadline,done,description,budget",
						"schedule", "schedule.id={}".format(schedule_id))
		print(result)
		form.name.data = result[0]
		form.deadline.data = result[1]
		form.done.data = result[2]
		form.description.data = result[3]
		form.budget.data = result[4]
		return render_template("member_edit_schedule_page.html", form=form, result=result)


@member_edit.route("/member/edit/equipment/<equipment_id>", methods=['GET', 'POST'])
def member_edit_equipment_page(equipment_id):
	auth = session.get('auth_type')
	if(auth != "Team leader" and auth != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	team_id = session.get("team_id")
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
	form = EditEquipmentForm()
	form.subteam.choices = subteams
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/equipments')
	if (request.method == 'POST' and form.submit_edit_equipment.data or form.validate()):
		name = form.name.data
		link = form.link.data
		purchasedate = form.purchasedate.data
		available = form.available.data
		subteam_id = form.subteam.data
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(equipment_id, date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(equipment_id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(equipment_id)):
					print("deleting", im)
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash("Please upload a file in JPG format", 'danger')

		update("equipment", "name='{}',link='{}',purchasedate='{}',available='{}',picture={}, team_id='{}',subteam_id={}".format(
			name, link, purchasedate, available, equipment_id, team_id, subteam_id), where="id={}".format(equipment_id))
		return redirect(url_for("team.team_equipments_page"))
	else:
		img_name = None
		for img in os.listdir(imageFolderPath):
			if(equipment_id in img[0:len(equipment_id)] and (img[len(equipment_id)] == '_' or img[len(equipment_id)] == '.')):
				img_name = img
		result = select("equipment.name,link,purchasedate,available,subteam.id",
						"equipment join subteam on equipment.subteam_id=subteam.id", "equipment.id={}".format(equipment_id))
		print(result)
		form.name.data = result[0]
		form.link.data = result[1]
		form.purchasedate.data = result[2]
		form.available.data = result[3]
		form.subteam.data = result[4]
		return render_template("member_edit_equipment_page.html", form=form, uploadImg=imageForm, result=result, imgName=img_name)


@member_edit.route("/member/edit/design/<design_id>", methods=['GET', 'POST'])
def member_edit_design_page(design_id):
	auth = session.get('auth_type')
	if(auth != "Team leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))

	typs = select("vehicle_type.id,vehicle_type.name",
				  "vehicle_type")

	team_id = session.get('team_id')
	member_id = session.get('member_id')
	form = EditDesignForm()
	form.typ.choices = typs

	if (request.method == 'POST' and form.submit_edit_design.data or form.validate()):
		name = form.name.data
		year = form.year.data
		maxspeed = form.maxspeed.data
		weight = form.weight.data
		duration = form.duration.data
		is_autonomous = form.is_autonomous.data
		typ = form.typ.data
		update("design", "name='{}',year='{}',maxspeed='{}',weight='{}',duration='{}', is_autonomous='{}', team_id='{}', type_of_vehicle = '{}'".format(
			name, year, maxspeed, weight, duration, is_autonomous, team_id, typ), where="id={}".format(design_id))
		return redirect(url_for("visitor.visitor_teaminfo_page"))
	else:
		result = select("design.name,year,maxspeed,weight,duration,is_autonomous,vehicle_type.id",
						"design join vehicle_type on design.type_of_vehicle=vehicle_type.id", "design.id={}".format(design_id))
		print(result)
		form.name.data = result[0]
		form.year.data = result[1]
		form.maxspeed.data = result[2]
		form.weight.data = result[3]
		form.duration.data = result[4]
		form.is_autonomous.data = result[5]
		form.typ.data = result[6]
		return render_template("member_edit_design_page.html", form=form, result=result)


@member_edit.route("/member/edit/sponsor/<sponsor_id>", methods=['GET', 'POST'])
def member_edit_sponsor_page(sponsor_id):
	auth = session.get('auth_type')
	sponsortypechoices = select(
		"sponsortype.id,sponsortype.name", "sponsortype")
	form = EditSponsorForm()
	form.typ.choices = sponsortypechoices
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/sponsors')
	if(auth != "Team leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	if (request.method == 'POST' and form.submit_edit_sponsor.data or form.validate()):
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
					print("deleting", im)
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash("Please upload a file in JPG format", 'danger')
		print(name, description, address, field, country, type_id)
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
		return render_template("member_edit_sponsor_page.html", form=form, uploadImg=imageForm, result=result, imgName=img_name)


@member_edit.route("/member/profile", methods=['GET', 'POST'])
def member_profile_page():
	auth = session.get('auth_type')
	if(auth != 'Member' and auth != 'Team leader' and auth != 'Subteam leader'):
		flash("Not authorized...", "danger")
		return redirect(url_for("home.home_page"))
	form = EditProfileForm()
	majors = select("major.id,major.name", "major")
	auth_types = select("id,name", "auth_type")
	form.major.choices = majors
	form.auth_type.choices = auth_types
	imgForm = UploadImageForm()
	cvForm = UploadCVForm()
	team_id = session.get('team_id')
	member_id = session.get('member_id')
	person_id = select(
		"person.id", "person join member on member.person_id=person.id", "member.id={}".format(member_id))[0]
	cvPath = None
	cvFolder = os.path.join(os.getcwd(), 'static/cv')
	imgPath = None
	imgFolder = os.path.join(os.getcwd(), 'static/images/person')

	if (request.method == 'POST' and form.submit_edit_profile.data or form.validate()):
		name = form.name.data
		email = form.email.data
		address = form.address.data
		phone = form.phone.data
		major = form.major.data
		clas = form.clas.data
		age = form.age.data
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
			# update persons cv file name
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
		majorID = select("major.id", "major", "id='{}'".format(major))[0]
		print("MAJORRRR", majorID)
		update("person", "name='{}', email='{}',phone='{}', class={}, age={}, major_id={}".format(
			name, email, phone, clas, age, majorID), "id={}".format(person_id))
		update("member", "address='{}'".format(
			address), "id={}".format(member_id))

		return redirect(url_for("member_edit.member_profile_page"))
	else:
		result = select("person.name,person.email,team.name,subteam.name,member.role,member.active, \
						member.entrydate,auth_type.id,member.address,person.phone,major.id, \
						person.class,person.age,person.cv,member.picture",
						"person join member on member.person_id=person.id \
						join team on person.team_id=team.id \
						join subteam on person.subteam_id=subteam.id \
						join auth_type on person.auth_type=auth_type.id \
						join major on person.major_id=major.id	",
						"member.id={}".format(member_id))
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
		imgPath = result[14]

		return render_template("member_profile_page.html", form=form, imgForm=imgForm, cvForm=cvForm, cvPath=cvPath, imgPath=imgPath)
