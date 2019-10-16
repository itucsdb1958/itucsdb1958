from flask import Flask,render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db
from dbinit import initialize,DATABASE_URL
import os

from home import home

app = Flask(__name__)

app.register_blueprint(home)




DEBUG = False
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
    url = DATABASE_URL
    initialize(url)


if __name__ == "__main__":
    app.run(debug = True)
