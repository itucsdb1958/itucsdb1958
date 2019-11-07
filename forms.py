from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, PasswordField
from wtforms import RadioField, IntegerField,FloatField, SelectMultipleField
from wtforms import HiddenField,SubmitField, BooleanField, FileField
from wtforms import widgets, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField,DateField

import re
auth_type_choices = [('3','Team Leader'),
                        ('4','Subteam Leader'), 
                        ('1','Member')]
major_choices = [('blg','Computer Engineering'),
                ('ehb','Electronics and Communication'),
                ('kon','Control and Automation Engineering'),
                ('uck','Aeronautical Engineering'),
                ('end','Industrial Engineering')]


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
    role = StringField('Role',validators=[DataRequired()])
    auth_type = SelectField('Authentication', choices=auth_type_choices,validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    name = StringField('Full Name',validators=[DataRequired()])
    address = StringField('Address')
    active = BooleanField('Active')
    entry = DateField('Entry Date',format='%Y-%m-%d')
    age = IntegerField('Age')
    phone = StringField('Phone',validators=[DataRequired()])
    clas = IntegerField('Class')
    major = SelectField('Major',choices=major_choices,validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class UploadCVForm(FlaskForm):
    cv = FileField(u'CV File',[validators.regexp(u'^[^/\\]\.pdf$]')])