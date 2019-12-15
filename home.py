# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db
from forms import *
from queries import select

home= Blueprint(name='home', import_name=__name__,
                    template_folder='templates')

@home.route("/")
def home_page():
    teams = select(columns="team.name,competition.name,team.email,team.adress,team.id,team.logo",
                   table="team left outer join competition on team.competition_id=competition.id order by team.name desc")
    return render_template("home_page.html", teams=teams)
