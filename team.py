import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select

team = Blueprint(name='team', import_name=__name__,
                    template_folder='templates')


@team.route("/schedule/")
@team.route("/schedule")
def team_schedule_page():
    schedule = select(
        columns="schedule.name,schedule.deadline,schedule.done,schedule.description,person.name", 
        table="schedule join member on schedule.member_id=member.id join person on person.id=member.person_id order by schedule.done,schedule.deadline")
    return render_template("schedule_page.html", schedule=schedule)

@team.route("/equipments/")
def team_equipments_page():
    auth = session.get('auth_type')
    if(auth != 'Team leader' and auth != 'Member' and auth!='Subteam leader'):
        flash('unauth','danger')
        return redirect(url_for("home.home_page"))
    
    equipments = select(
        columns="equipment.name,equipment.link,equipment.purchasedate,equipment.available,equipment.picture,subteam.name", 
        table="equipment join team on equipment.team_id = team.id join subteam on equipment.subteam_id=subteam.id",
        where="team.id = {}".format(session.get("team_id"))
        )
    return render_template("equipments_page.html", equipments=equipments)