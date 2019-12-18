import os

import psycopg2 as db
import psycopg2.extensions
from flask import Blueprint, Flask, render_template, redirect, url_for

from admin_add import admin_add
from admin_delete import admin_delete
from admin_edit import admin_edit
from admin_list import admin_list
from dbinit import initialize
from home import home
from login import login
from member_add import member_add
from member_delete import member_delete
from member_edit import member_edit
from member_list import member_list
from member_profile import member_profile
from panel import panel
from team import team
from visitor import visitor

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

RELEASE = True

if(not RELEASE):
    os.environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
    initialize(os.environ.get('DATABASE_URL'))

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(member_profile)
app.register_blueprint(admin_list)
app.register_blueprint(admin_edit)
app.register_blueprint(admin_add)
app.register_blueprint(admin_delete)
app.register_blueprint(member_list)
app.register_blueprint(member_add)
app.register_blueprint(member_delete)
app.register_blueprint(member_edit)
app.register_blueprint(visitor)
app.register_blueprint(team)
app.register_blueprint(panel)


@app.errorhandler(404)
def not_found(e):
    return render_template("error_404.html")

@app.errorhandler(500)
def server_error(e):
    return render_template("error_500.html")

if __name__ == "__main__":
    if(not RELEASE):
        app.run(debug=True)
    else:
        app.run()
