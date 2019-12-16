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

admin_list = Blueprint(name='admin_list', import_name=__name__)


@admin_list.route("/admin/sql/", methods=['GET', 'POST'])
@admin_list.route("/admin/sql", methods=['GET', 'POST'])
def sql_page():
    form = SQLForm()
    if form.validate_on_submit():
        query = form.query.data
        result = run(query)
        return render_template('sql_page.html', form=form, queryResult=result, resultLen=len(result))
    return render_template('sql_page.html', form=form, queryResult=None, resultLen=0)

@admin_list.route("/admin/teams/")
@admin_list.route("/admin/teams")
def admin_teams_page():
    if(session.get('auth_type') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        result = select(columns="team.name,team.email,team.num_members,team.found_year,competition.name,team.id",
                        table="team left outer join competition on team.competition_id=competition.id \
							order by team.name asc")
        return render_template('admin_teams_page.html', teams=result) 

@admin_list.route("/admin/members/")
@admin_list.route("/admin/members")
def admin_members_page():
    if(session.get('auth_type') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        result = select(columns="person.name,person.email,auth_type.name,team.name,person.id",
                        table="person join team on person.team_id=team.id \
							join auth_type on person.auth_type=auth_type.id \
							order by team.name asc, auth_type.name desc")
        return render_template('admin_members_page.html', members=result)
