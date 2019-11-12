import re

from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, FloatField, HiddenField,
                     IntegerField, PasswordField, RadioField, SelectField,
                     SelectMultipleField, StringField, SubmitField,
                     TextAreaField, validators, widgets)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from queries import select

auth_type_choices = [('3', 'Team Leader'),
                     ('4', 'Subteam Leader'),
                     ('1', 'Member')]
major_choices = [('blg', 'Computer Engineering'),
                 ('ehb', 'Electronics and Communication'),
                 ('kon', 'Control and Automation Engineering'),
                 ('uck', 'Aeronautical Engineering'),
                 ('end', 'Industrial Engineering')]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SQLForm(FlaskForm):
    query = TextAreaField('SQL to be run', validators=[DataRequired()])
    submit = SubmitField('Run query')


class EditMemberForm(FlaskForm):
    team = StringField('Team', validators=[DataRequired()])
    subteam = StringField('Subteam', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    auth_type = SelectField(
        'Authentication', choices=auth_type_choices, validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired()])
    address = StringField('Address')
    active = BooleanField('Active')
    entry = DateField('Entry Date', format='%Y-%m-%d')
    age = IntegerField('Age')
    phone = StringField('Phone', validators=[DataRequired()])
    clas = IntegerField('Class')
    major = SelectField('Major', choices=major_choices,
                        validators=[DataRequired()])
    submit_member = SubmitField('Update Profile')


class EditTeamForm(FlaskForm):
    name = StringField('Team Name')
    memberCtr = StringField('Member Number')
    year = StringField('Foundation Year')
    email = StringField('Email')
    address = StringField('Address')
    res = select('id,name', 'competition')
    competition = SelectField(
        'Competition', choices=res)
    submit_team = SubmitField('Update Team')


class EditCompetitionForm(FlaskForm):
    name = StringField("Competition Name")
    date = DateField("Date")
    country = StringField("Country")
    description = TextAreaField("Description")
    reward = StringField("Reward")
    submit_competition = SubmitField("Update Team")


class UploadCVForm(FlaskForm):
    cv = FileField(u'CV File')


class UploadImageForm(FlaskForm):
    image = FileField(u'Image File')
