# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import Blueprint, redirect, render_template, url_for,session,flash,request

from forms import AddTeamForm
from queries import insert

admin_add = Blueprint(name='admin_add', import_name=__name__)


@admin_add.route("/admin/add/team", methods=['GET', 'POST'])
def admin_add_team_page():
    if(session.get('auth_type') != 'admin'):
        flash('No admin privileges...', 'danger')
        return redirect(url_for('home.home_page'))
    else:
        form = AddTeamForm()
        if (request.method == 'POST' and form.submit_add_team.data or form.validate()):
            name = form.name.data
            email = form.mail.data
            address = form.address.data
            year = form.year.data
            insert("team", "name,num_members,found_year,email,adress,logo,competition_id",
                   "'{}',0,'{}','{}','{}','-1',NULL".format(name, year, email, address))
            return redirect(url_for('admin_add.admin_add_team_page'))
        return render_template('admin_add_team_page.html', imgName=None, form=form)
