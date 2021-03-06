from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)
from forms import *
from queries import insert, select

member_add = Blueprint(name='member_add', import_name=__name__,
                       template_folder='templates')


@member_add.route("/member/add/member", methods=['GET', 'POST'])
def member_add_member_page():
    if(session.get('auth_type') != "Team leader"):
        flash("Not an authorized person", 'danger')
        return redirect(url_for("home.home_page"))
    team_id = session.get('team_id')
    subteams = select("subteam.id,subteam.name",
                      "subteam join team on subteam.team_id=team.id", "team.id={}".format(team_id))
    form = AddMemberForm()
    form.subteam.choices = subteams
    majors = select("id,name", "major")
    form.major.choices = majors
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
        major_id = select("id", "major", "id='{}'".format(major))[0]
        insert("person", "NAME, AGE, PHONE, CV, EMAIL, CLASS, AUTH_TYPE, STATUS, TEAM_ID, SUBTEAM_ID, MAJOR_ID",
               "'{}','{}','{}','-1','{}',{},1,{},{},{},{}".format(
                   name, age, phone, mail, clas, status, team_id, subteam, major_id
               ))
        person_id = select("id", "person", "name='{}'".format(name))[0]
        insert("member", "ROLE, ENTRYDATE, ACTIVE, PICTURE, ADDRESS, PERSON_ID",
               "'Uye',CURRENT_DATE,true,'-1.png','Address',{}".format(person_id))
        member_id = select("id", "member", "person_id={}".format(person_id))[0]
        insert("users", "username,password,member_id",
               "'{}',crypt('1234',gen_salt('bf')),{}".format(username, member_id))
        return redirect(url_for("member_add.member_add_member_page"))
    return render_template("member_add_member_page.html", form=form)


@member_add.route("/member/add/competition", methods=['GET', 'POST'])
def member_add_competition_page():
    auth = session.get('auth_type')
    if(auth != "Team leader"):
        flash("Not an authorized person", 'danger')
        return redirect(url_for("home.home_page"))
    form = AddCompetitionForm()
    if (request.method == 'POST' and form.submit_add_competition.data or form.validate()):
        name = form.name.data
        description = form.description.data
        reward = form.reward.data
        date = form.date.data
        country = form.country.data

        insert("competition", "name,date,country,description,reward,team_id",
               "'{}','{}','{}','{}','{}',{}".format(name, date, country, description, reward, session.get('team_id')))

    return render_template("member_add_competition_page.html", form=form)


@member_add.route("/member/add/design", methods=['GET', 'POST'])
def member_add_design_page():
    auth = session.get('auth_type')
    if(auth != "Team leader"):
        flash("Not an authorized person", 'danger')
        return redirect(url_for("home.home_page"))
    form = AddDesignForm()
    team_id = session.get("team_id")
    typ = select("vehicle_type.id,vehicle_type.name",
                 "vehicle_type")
    form = AddDesignForm()
    form.typ.choices = typ
    if (request.method == 'POST' and form.submit_add_design.data or form.validate()):
        name = form.name.data
        year = form.year.data
        maxspeed = form.maxspeed.data
        weight = form.weight.data
        duration = form.duration.data
        is_autonomous = form.is_autonomous.data
        type_id = form.typ.data
        insert("design", "NAME, YEAR, MAXSPEED, WEIGHT, DURATION, IS_AUTONOMOUS, TEAM_ID, TYPE_OF_VEHICLE",
               "'{}','{}','{}','{}','{}','{}','{}','{}'".format(
                   name, year, maxspeed, weight, duration, is_autonomous, team_id, type_id
               ))

        return redirect(url_for("member_add.member_add_design_page"))
    return render_template("member_add_design_page.html", form=form)


@member_add.route("/member/add/sponsor", methods=['GET', 'POST'])
def member_add_sponsor_page():
    auth = session.get('auth_type')
    sponsortypechoices = select(
        "sponsortype.id,sponsortype.name", "sponsortype")
    form = AddSponsorForm()
    form.typ.choices = sponsortypechoices
    if(auth != "Team leader"):
        flash("Not an authorized person", 'danger')
        return redirect(url_for("home.home_page"))
    if (request.method == 'POST' and form.submit_add_sponsor.data or form.validate()):
        name = form.name.data
        description = form.description.data
        address = form.address.data
        field = form.field.data
        country = form.country.data
        type_id = form.typ.data
        insert("sponsor", "name,description,field,country,logo,address,type_id",
               "'{}','{}','{}','{}','-1.png','{}',{}".format(name, description, field, country, address, type_id))
        return redirect(url_for("member_add.member_add_sponsor_page"))
    return render_template("member_add_sponsor_page.html", form=form)


@member_add.route("/member/add/equipment", methods=['GET', 'POST'])
def member_add_equipment_page():
    auth = session.get('auth_type')

    if(auth != "Team leader" and auth != "Subteam leader"):
        flash("Not an authorized person", 'danger')
        return redirect(url_for("home.home_page"))
    team_id = session.get('team_id')

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
               "'{}','{}','{}','{}','-1.png','{}','{}'".format(
                   name, link, purchasedate, available, team_id, subteam_id
               ))

        return redirect(url_for("member_add.member_add_equipment_page"))
    return render_template("member_add_equipment_page.html", form=form)


@member_add.route("/member/add/schedule", methods=['GET', 'POST'])
def member_add_schedule_page():
    auth = session.get('auth_type')
    print(auth)
    if(auth != "Team leader" and auth != "Subteam leader"):
        flash("Not an authorized person", 'danger')
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
    if(session['auth_type'] != "Team leader" and session['auth_type'] != "Subteam leader" and session['auth_type'] != "Member"):
        flash("Not an authorized person", 'danger')
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
               "'{}','{}','{}','{}','-1.png',{},{}".format(name, area, description, link, isvideo, member_id))
        return redirect(url_for("visitor.visitor_tutorials_page"))
    return render_template("member_add_tutorial_page.html", form=form)
