from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import delete

member_delete = Blueprint(name='member_delete', import_name=__name__,
                          template_folder='templates')


@member_delete.route("/member/delete/competition/<competition_id>", methods=['GET', 'POST'])
def member_delete_competition_page(competition_id):
    auth = session.get('auth_type')
    if(auth != "Team leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    delete(table="competition", where="id={}".format(competition_id))
    return redirect(url_for("home.home_page"))


@member_delete.route("/member/delete/sponsor/<sponsor_id>", methods=['GET', 'POST'])
def member_delete_sponsor_page(sponsor_id):
    auth = session.get('auth_type')
    if(auth != "Team leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    delete(table="sponsor", where="id={}".format(sponsor_id))
    return redirect(url_for("home.home_page"))

@member_delete.route("/member/delete/design/<design_id>", methods=['GET', 'POST'])
def member_delete_design_page(design_id):
    auth = session.get('auth_type')
    if(auth != "Team leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    delete(table="design", where="id={}".format(design_id))
    return redirect(url_for("visitor.visitor_teaminfo_page"))

@member_delete.route("/member/delete/member/<person_id>", methods=['GET', 'POST'])
def member_delete_member_page(person_id):
    auth = session.get('auth_type')
    if(auth != "Team leader" and auth != 'admin'):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    result = select("member.id,users.username",
                    "member join users on users.member_id=member.id join person on member.person_id=person.id", where="person.id={}".format(person_id))
    member_id, username = result[0], result[1]
    delete("users", "username='{}'".format(username))
    delete("member", "id={}".format(member_id))
    delete(table="person", where="id={}".format(person_id))
    return redirect(url_for("member_list.member_list_members_page"))


@member_delete.route("/member/delete/equipment/<equipment_id>", methods=['GET', 'POST'])
def member_delete_equipment_page(equipment_id):
    auth = session.get('auth_type')
    if(auth != "Team leader" and auth != "admin" and auth != "Subteam leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    delete(table="equipment", where="id={}".format(equipment_id))
    return redirect(url_for("team.team_equipments_page"))


@member_delete.route("/member/delete/schedule/<schedule_id>", methods=['GET', 'POST'])
def member_delete_schedule_page(schedule_id):
    auth = session.get('auth_type')
    if(auth != "Team leader" and auth != "admin" and auth != "Subteam leader"):
        flash("Not an authorized person")
        return redirect(url_for("home.home_page"))
    delete(table="schedule", where="id={}".format(schedule_id))
    return redirect(url_for("team.team_schedule_page"))


@member_delete.route("/member/delete/tutorial/<tutorial_id>", methods=['GET', 'POST'])
def member_delete_tutorial_page(tutorial_id):
    auth = session.get('auth_type')
    member_id = session.get('member_id')

    if(auth != "Team leader" and auth != "admin" and auth != "Subteam leader" and auth != "Member"):
        flash("Not an authorized person")
        return redirect(url_for("visitor.visitor_tutorials_page"))
    if(member_id == select("member_id", "tutorial", "id={}".format(tutorial_id))[0]):
        delete(table="tutorial", where="id={}".format(tutorial_id))
    else:
        flash("Not an authorized person")
        return redirect(url_for("visitor.visitor_tutorials_page"))
    return redirect(url_for("visitor.visitor_tutorials_page"))
