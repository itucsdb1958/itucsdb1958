# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select
import os
visitor = Blueprint(name='visitor', import_name=__name__,
                    template_folder='templates')

# TODO:: IMPLEMENT SMALL LOGO OF EACH ROUTE'S ELEMENTS


@visitor.route("/competitions/")
@visitor.route("/competitions")
def visitor_competitions_page():
    competitions = select("*", "competition order by name")
    print("BUARDA:..")
    print(competitions[0][-2])
    print(competitions[0][-1])
    return render_template("competitions_page.html", competitions=competitions)


@visitor.route("/teams/")
@visitor.route("/teams")
def visitor_teams_page():
    teams = select(columns="team.name,competition.name,team.email,team.adress,team.id",
                   table="team left outer join competition on team.competition_id=competition.id order by team.name desc")[0]
    return render_template("teams_page.html", teams=teams)


@visitor.route("/sponsors/")
@visitor.route("/sponsors")
def visitor_sponsors_page():
    # made a change for sponsor page . INCLUDE THIS COMMIT
    sponsors = select(
        "name,description,field,country,logo,address,id", "sponsor order by name asc")[0]
    return render_template("sponsors_page.html", sponsors=sponsors)


@visitor.route("/schedule/")
@visitor.route("/schedule")
def visitor_schedule_page():
    auth = session.get('auth_type')
    if(auth != 'Team leader' and auth != 'Subteam leader' and auth != 'Member'):
        flash("Unauth", 'danger')
        return redirect(url_for("home.home_page"))
    member_id = session.get('member_id')
    schedule = select(
        columns="schedule.name,schedule.deadline,schedule.done,schedule.description,person.name,schedule.id",
        table="schedule join member on schedule.member_id=member.id join person on person.id=member.person_id", 
		where="member.id={} order by schedule.done,schedule.deadline".format(member_id))[0]
    return render_template("schedule_page.html", schedule=schedule)


@visitor.route("/teaminfo/<team_id>")
def visitor_teaminfo_page(team_id):

    teaminfo = select(
        columns="team.name,team.num_members,team.found_year,team.email,team.adress,team.logo",
        table="team",
        # the selected team
        where="id = {}".format(team_id)
    )[0]
    team_designs = select(
        columns="design.name,design.year,design.maxspeed,design.weight,design.duration,design.is_autonomous,design.id",
        table="design join team on design.team_id=team.id",
        where="team.id = {}".format(team_id)
    )
    competition = select(
        columns="competition.name,competition.date,competition.country,competition.description,competition.reward",
        table="team join competition on team.competition_id=competition.id",
        where="team.id = {}".format(team_id)
    )[0]
    members_info = select(
        columns="person.name,person.age,person.phone,person.cv,person.email,person.class,member.picture,subteam.name",
        table="team join person on team.id=person.team_id join member on member.person_id=person.id join subteam on person.subteam_id=subteam.id",
        where="team.id = {}".format(team_id)
    )[0]
    print("Member info",members_info)
    sponsors = select(
        columns="sponsor.name,sponsortype.name,sponsor.logo",
        table="team join sponsorindex on team.id=sponsorindex.team_id join sponsor on sponsor.id=sponsorindex.sponsor_id join sponsortype on sponsortype.id=sponsor.type_id",
        where="team.id = {}".format(team_id)
    )[0]
    return render_template("teaminfo_page.html", teaminfo=teaminfo, team_designs=team_designs, competition=competition, members_info=members_info, sponsors=sponsors)


@visitor.route("/tutorials/")
@visitor.route("/tutorials")
def visitor_tutorials_page():
    tutorials = select(
        columns="tutorial.name,tutorial.area,tutorial.description,tutorial.link,tutorial.picture,person.name,member_id,tutorial.id",
        table="tutorial join member on tutorial.member_id=member.id join person on person.id=member.person_id order by tutorial.name")[0]
    return render_template("tutorials_page.html", tutorials=tutorials)
