from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, session, url_for)

from forms import *
from queries import insert, select

member_add = Blueprint(name='member_add', import_name=__name__,
					   template_folder='templates')


@member_add.route("/member/add/member", methods=['GET', 'POST'])
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
		member_id = select("id", "member", "person_id={}".format(person_id))[0]
		insert("users", "username,password,member_id",
			   "'{}',crypt('1234',gen_salt('bf')),{}".format(username, member_id))
		return redirect(url_for("member_add.member_add_member_page"))
	return render_template("member_add_member_page.html", form=form)


@member_add.route("/member/add/competition", methods=['GET', 'POST'])
def member_add_competition_page():
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


@member_add.route("/member/add/sponsor", methods=['GET', 'POST'])
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
		return redirect(url_for("member_add.member_add_sponsor_page"))
	return render_template("member_add_sponsor_page.html", form=form)


@member_add.route("/member/add/equipment", methods=['GET', 'POST'])
def member_add_equipment_page():
	auth = session.get('auth_type')

	if(auth != "Team leader" and auth != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))
	team_id = session.get("team_id")
	subteams = select("subteam.id,subteam.name",
					  "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
	form = AddEquipmentForm()
	form.subteam.choices = subteams
	if (request.method == 'POST' and form.submit_add_equipment.data or form.validate()):
		name = form.name.data
		link = form.link.data
		purchasedate = form.purchasedate.data
		available = form.available.data
		subteam_id = form.subteam.data
		insert("equipment", "NAME, LINK, PURCHASEDATE, AVAILABLE, PICTURE, TEAM_ID, SUBTEAM_ID",
			   "'{}','{}','{}','{}','-1','{}','{}'".format(
				   name, link, purchasedate, available, team_id, subteam_id
			   ))

		return redirect(url_for("member_add.member_add_equipment_page"))
	return render_template("member_add_equipment_page.html", form=form)


@member_add.route("/member/add/schedule", methods=['GET', 'POST'])
def member_add_schedule_page():
	auth = session.get('auth_type')
	print(auth)
	if(auth != "Team leader" and auth != "Subteam leader"):
		flash("Not an authorized person")
		return redirect(url_for("home.home_page"))

	member_id = session.get('member_id')
	form = AddScheduleForm()
	if (request.method == 'POST' and form.submit_add_schedule.data or form.validate()):
		name = form.name.data
		deadline = form.deadline.data
		done = form.done.data
		description = form.description.data
		budget = form.budget.data

		insert("schedule", "NAME, DEADLINE, DONE, DESCRIPTION, BUDGET, MEMBER_ID",
			   "'{}','{}','{}','{}','{}',{}".format(
				   name, deadline, done, description, budget, member_id
			   ))

		return redirect(url_for("member_add.member_add_schedule_page"))
	return render_template("member_add_schedule_page.html", form=form)

@member_add.route("/member/add/tutorial", methods=['GET', 'POST'])
def member_add_tutorial_page():
    if(session['auth_type'] != "Team leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))

    form = AddTutorialForm()
    if (request.method == 'POST' and form.submit_add_tutorial.data or form.validate()):
        name = form.name.data
        area = form.area.data
        description = form.description.data
        link = form.link.data
        isvideo = form.isvideo.data
        member_id = session.get('member_id')

        insert("tutorial", "NAME, AREA, DESCRIPTION, LINK, PICTURE, ISVIDEO, MEMBER_ID",
               "'{}','{}','{}','{}','avatar',{},{}".format(name, area, description, link, isvideo, member_id))
        return redirect(url_for("visitor.visitor_tutorials_page"))
    return render_template("member_add_tutorial_page.html", form=form)
