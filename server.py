from dbinit import initialize
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db
from os import environ

from home import home
from login import login, logout
from admin import sqlpage
from member_profile import member_profile

RELEASE = False

if(not RELEASE):
    environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
    initialize(environ.get('DATABASE_URL'))

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(sqlpage)
app.register_blueprint(member_profile)

if __name__ == "__main__":
    if(not RELEASE):
        app.run(debug=True)
    else:
        app.run()
