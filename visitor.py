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