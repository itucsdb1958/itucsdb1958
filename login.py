# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from forms import LoginForm
import psycopg2 as db
from Crypto.Hash import SHA256
import os
from queries import select
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
            session.pop('auth_type', None)
            session.pop('team_id', None)
            session.pop('member', None)
            flash('You have been successfully logged out.', 'success')

        except:
            flash('Logging out is not completed.','danger')
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
        print("LOGIN RESULT",result)
        if((result != None) and (len(result) >= 1)):
            flash('You have been logged in!', 'success')
            session['logged_in'] = True
            session['username'] = username
            session['member_id'] = result[2]
            session['team_id'] = select(
                "team.id", "team join person on person.team_id=team.id join member on member.person_id=person.id", "member.id={}".format(result[2]))[0]
            print("HEREEE",session.get('team_id'))
            session['auth_type'] = select(
                "auth_type.name", "person join member on member.person_id=person.id join auth_type on person.auth_type=auth_type.id", "member.id={}".format(result[2]))[0]
            print("GIRISTEKI AUTH TYPE:",session.get('auth_type'),session.get('team_id'))
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
            session['team_id'] = '-1'
            session['auth_type'] = 'admin'
            success = True
            return redirect(url_for('home.home_page'))
    except db.DatabaseError:
        connection.rollback()
        flash('Login Unsuccessful. Please check username and password', 'danger')
    finally:
        connection.close()
        return success
