from flask import Flask,render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db
from dbinit import initialize,DATABASE_URL
import os

from home import home
from login import login,logout

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(login)
app.register_blueprint(logout)



DEBUG = False
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
    url = DATABASE_URL
    initialize(url)


if __name__ == "__main__":
    app.run(debug = True)
