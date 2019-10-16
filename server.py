from dbinit import initialize
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
import psycopg2 as db

from home import home
from login import login, logout

from os import environ

DEBUG_MODE = True
RELEASE = False

if(not RELEASE):
    environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
initialize(environ.get('DATABASE_URL'))


app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(logout)

# initialize the local database


if __name__ == "__main__":
    if(DEBUG_MODE):
        app.run(debug=True)
    else:
        app.run()
