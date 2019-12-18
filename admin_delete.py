import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

from member_profile import Member
from queries import delete, run, select, update

admin_delete = Blueprint(name='admin_delete', import_name=__name__)

@admin_delete.route("/admin/delete/team/<team_id>", methods=['GET', 'POST'])
def admin_delete_team_page(team_id):
	auth = session.get('auth_type')
	if(auth != "admin"):
		flash("Not an authorized person",'danger')
		return redirect(url_for("home.home_page"))
	delete(table="team", where="id={}".format(team_id))
	return redirect(url_for("admin_list.admin_teams_page"))
    