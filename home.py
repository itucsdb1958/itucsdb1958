# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session,abort,Blueprint
import psycopg2 as db

home= Blueprint(name='home', import_name=__name__)

@home.route("/")
def home_page():
	return render_template('home_page.html')
