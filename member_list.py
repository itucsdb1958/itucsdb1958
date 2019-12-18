# -*- coding: utf-8 -*-
import math
import os
import time

import psycopg2 as db
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from queries import select

member_list = Blueprint(name='member_list', import_name=__name__,
                        template_folder='templates')


@member_list.route("/member/members")
def member_list_members_page():
    auth = session.get('auth_type')
    if(auth != "Team leader" and auth!= 'Member' and auth!='Subteam leader'):
       flash("Not an authorized person",'danger')
        return redirect(url_for("home.home_page"))
    members = select(columns="person.name,person.email,auth_type.name,team.name,person.id",
                     table="person join team on person.team_id=team.id \
							join auth_type on person.auth_type=auth_type.id",
                     where="team.id={} order by team.name asc, auth_type.name desc".format(session.get('team_id')))
    return render_template("member_members_page.html", members=members)
