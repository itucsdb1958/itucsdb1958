# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
from forms import AddMemberForm, AddCompetitionForm
from queries import select, insert

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
               "'{}','{}','{}','{}','{}'".format(name,date,country,description,reward))

    return render_template("member_add_competition_page.html", form=form)
