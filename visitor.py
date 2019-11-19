# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select

visitor = Blueprint(name='visitor', import_name=__name__,
                    template_folder='templates')

# TODO:: IMPLEMENT SMALL LOGO OF EACH ROUTE'S ELEMENTS


@visitor.route("/competitions/")
@visitor.route("/competitions")
def visitor_competitions_page():
    competitions = select("*", "competition")
    return render_template("competitions_page.html", competitions=competitions)


@visitor.route("/teams/")
@visitor.route("/teams")
def visitor_teams_page():
    teams = select(columns="team.name,competition.name,team.email,team.adress,team.id",
                   table="team join competition on team.competition_id=competition.id order by team.name desc")
    return render_template("teams_page.html", teams=teams)


@visitor.route("/sponsors/")
@visitor.route("/sponsors")
def visitor_sponsors_page():
    sponsors = select(
        "name,description,field,country,logo,address", "sponsor order by name asc")
    return render_template("sponsors_page.html", sponsors=sponsors)


@visitor.route("/schedule/")
@visitor.route("/schedule")
def visitor_schedule_page():
    schedule = select(
        columns="schedule.name,schedule.deadline,schedule.done,schedule.description,person.name", 
        table="schedule join member on schedule.member_id=member.id join person on person.id=member.person_id order by schedule.done,schedule.deadline")
    return render_template("schedule_page.html", schedule=schedule)


@visitor.route("/teaminfo/")
@visitor.route("/teaminfo")
def visitor_teaminfo_page():
    teaminfo = select(
        columns="team.name,team.num_members,team.found_year,team.email,team.adress,team.logo,team.competition_id",
        table = "team",
        #the selected team
        where="id = 3"
        )
    design = select(
        columns="design.name,design.year,design.maxspeed,design.weight,design.duration,design.is_autonomous",
        table="team join design on team.id=design.id",
        where="team.id = 3"
    )
    competition = select(
        columns="competition.name,competition.date,competition.country,competition.description,competition.reward",
        table="team join competition on team.competition_id=competition.id",
        where="team.id = 3"
    )   
    members = select(
        columns="person.name,person.age,person.phone,person.cv,person.email,person.class",
        table="team join person on team.id=person.team_id join member on member.person_id=person.id",
        where="team.id = 3"
    )
    sponsor = select(
        columns="sponsor.name,sponsortype.name,sponsor.logo",
        table="team join sponsorindex on team.id=sponsorindex.team_id join sponsor on sponsor.id=sponsorindex.sponsor_id join sponsortype on sponsortype.id=sponsor.type_id",
        where="team.id = 3"
    )
    return render_template("teaminfo_page.html",teaminfo=teaminfo, design=design, competition=competition, members=members, sponsor=sponsor)