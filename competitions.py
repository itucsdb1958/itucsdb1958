# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
from forms import *
import psycopg2 as db
from queries import select


competitions = Blueprint(name='competitions', import_name=__name__,template_folder='templates')

@competitions.route("/competitions")
def competitions_page():
    
    competitions = select("*","competition")
    return render_template("competitions_page.html",competitions = competitions)