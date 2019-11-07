# -*- coding: utf-8 -*-
import os
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

from forms import EditMemberForm, SQLForm, UploadCVForm
from member_profile import Member
from queries import run, select, update

admin = Blueprint(name='admin', import_name=__name__)


@admin.route("/admin")
def admin_page():
    if (session.get('member_id') == 'admin'):
        return render_template('admin_page.html')
    else:
        return redirect(url_for('home.home_page'))


@admin.route("/admin/sql", methods=['GET', 'POST'])
def sql_page():
    form = SQLForm()
    if form.validate_on_submit():
        query = form.query.data
        result = run(query)
        return render_template('sql_page.html', form=form, queryResult=result, resultLen=len(result))
    return render_template('sql_page.html', form=form, queryResult=None, resultLen=0)


@admin.route("/admin/competitions")
def admin_competitions_page():
    if(session.get('member_id') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        result = select(columns="*", table="competition order by name asc")
        return render_template('admin_competitions_page.html', competitions=result, length=len(result))


@admin.route("/admin/teams")
def admin_teams_page():
    if(session.get('member_id') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        result = select(columns="team.name,competition.name,team.email,team.adress",
                        table="team join competition on team.competition_id=competition.id order by team.name desc")
        return render_template('admin_teams_page.html', team=result, length=len(result))


@admin.route("/admin/members")
def admin_members_page():
    if(session.get('member_id') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        result = select(columns="person.name,person.email,auth_type.name,team.name,person.id",
                        table="person join team on person.team_id=team.id \
							join auth_type on person.auth_type=auth_type.id \
							order by team.name asc, auth_type.name desc")
        return render_template('admin_members_page.html', members=result, length=len(result))


@admin.route("/admin/members/edit/<id>", methods=['GET', 'POST'])
def admin_edit_member_page(id):
    # TODO:: FILE OPERATIONS ILE FOTO YUKLENECEK INDIRILECEK.
    # TODO:: Alter table to include social accounts links in person database.
    form = EditMemberForm()
    cvForm = UploadCVForm()
    cvPath = None
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
        print(cv.filename)
        if(cv and '.pdf' in cv.filename):
            print(dir(cv))
            filename = secure_filename("{}.pdf".format(id))
            filePath = os.path.join(os.getcwd(), 'static/cv', filename)
            if(os.path.exists(filePath)):
                os.remove(filePath)
            cv.save(filePath)
        elif(cv):
            flash("Please insert a pdf file.", 'danger')

        teamID = select(columns="id", table="team",
                        where="name='{}'".format(team))
        subteamID = select(columns="id", table="subteam",
                           where="name='{}'".format(subteam))
        majorID = select(columns="id", table="major",
                         where="code='{}'".format(major))
        memberID = select(columns="member.id",
                          table="member join person on member.person_id=person.id",
                          where="person.id={}".format(id))

        teamID, subteamID, majorID, memberID = teamID[0], subteamID[0], majorID[0], memberID[0]

        update("member", "role='{}', active={}, address='{}'".format(
            role, active, address), where="id={}".format(memberID))

        update("person", "name='{}', age='{}', phone='{}', cv={}, email='{}', \
					class={}, auth_type={}, team_id={}, subteam_id={}, major_id={}".format(
            name, age, phone, id, email, clas, auth_type, teamID, subteamID, majorID), where="id={}".format(id))

        return redirect(url_for('admin.admin_edit_member_page', id=id, cvPath=id))
    else:
        if(session.get('member_id') != 'admin'):
            flash('No admin privileges...', 'danger')
            return redirect(url_for('home.home_page'))
        else:
            columns = """person.name,person.email,team.name,subteam.name,\
					member.role,member.active,member.entrydate,auth_type.name, \
					member.address,person.phone,major.name,person.class,person.age,member.id,person.cv"""

            table = """member join person on member.person_id=person.id \
					join major on person.major_id=major.id \
					join team on person.team_id=team.id \
					join subteam on person.subteam_id=subteam.id \
					join auth_type on person.auth_type=auth_type.id"""

            where = "person.id={}".format(id)
            result = select(columns, table, where)

            cvPath = os.path.join(
                os.getcwd(), 'static/cv', "{}.pdf".format(id))
            cvPath = id if os.path.exists(cvPath) else None

            return render_template('admin_edit_member_page.html', form=form, upload=cvForm, result=result, cvPath=cvPath)

    return render_template('admin_edit_member_page.html', form=form, upload=cvForm, cvPath=cvPath)


@admin.route("/download/<filename>", methods=['GET', 'POST'])
def download(filename):
    cvFolder = os.path.join(admin.root_path, "static/cv")
    return send_from_directory(directory=cvFolder, filename=filename+".pdf", as_attachment=True)
