# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from forms import LoginForm
import psycopg2 as db
from Crypto.Hash import SHA256
import os

login = Blueprint(name='login', import_name=__name__,
                  template_folder='templates')


@login.route("/login", methods=['GET', 'POST'])
def login_page():
    if session.get('logged_in'):
        return redirect(url_for('home.home_page'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            memberLoginSuccesssul = checkMemberLogin(username, password)
            if(not memberLoginSuccesssul):
                adminLogin = checkAdminLogin(username, password)
            if(memberLoginSuccesssul or adminLogin):
                return redirect(url_for('home.home_page'))
        return render_template('login_page.html', form=form)


@login.route("/logout")
def logout_page():
    if 'logged_in' in session:
        try:
            session.pop('username', None)
            session['member_id'] = 0
            session.pop('logged_in', None)
            session.pop('member', None)
            flash('You have been successfully logged out.', 'success')

        except:
            flash('Logging out is not completed.')
    return redirect(url_for('home.home_page'))


def checkMemberLogin(username, password):
    success = False
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        statement = """SELECT * FROM USERS WHERE USERNAME = '%s' AND PASSWORD = crypt('%s',PASSWORD)
				""" % (username, password)
        cursor.execute(statement)
        result = cursor.fetchone()
        if((result != None) and (len(result) >= 1)):
            flash('You have been logged in!', 'success')
            session['logged_in'] = True
            session['username'] = username
            session['member_id'] = result[2]
            success = True
            return redirect(url_for('home.home_page'))
    except db.DatabaseError:
        connection.rollback()
        flash('Login Unsuccessful. Please check username and password', 'danger')
    finally:
        connection.close()
        return success


def checkAdminLogin(username, password):
    success = False
    try:
        connection = db.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        statement = """SELECT * FROM ADMIN WHERE USERNAME = '%s' AND PASSWORD = crypt('%s',PASSWORD)
				""" % (username, password)
        cursor.execute(statement)
        result = cursor.fetchone()
        if((result != None) and (len(result) >= 1)):
            flash('You have been logged in!', 'success')
            session['logged_in'] = True
            session['username'] = username
            session['member_id'] = 'admin'
            success = True
            return redirect(url_for('home.home_page'))
    except db.DatabaseError:
        connection.rollback()
        flash('Login Unsuccessful. Please check username and password', 'danger')
    finally:
        connection.close()
        return success
