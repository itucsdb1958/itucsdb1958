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

status_choices = [('1','Active'),('2','Disactive')]
class_choices = [('1','1'),('2','2'),('3','3'),('4','4')]
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SQLForm(FlaskForm):
    query = TextAreaField('SQL to be run', validators=[DataRequired()])
    submit = SubmitField('Run query')


class EditMemberForm(FlaskForm):
    team = StringField('Team', validators=[DataRequired()])
    subteam = SelectField('Subteam',coerce=int, validators=[DataRequired()])
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

class AddTeamForm(FlaskForm):
    name = StringField('Team Name',validators=[DataRequired()])
    year = DateField('Foundation Year')
    mail = EmailField('E-mail',validators=[DataRequired(), Email()])
    address = StringField('Address')
    submit_add_team = SubmitField('Add Team')

class AddMemberForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    age = StringField("Age",validators=[DataRequired()])
    phone= StringField("Phone",validators=[DataRequired()])
    mail = EmailField('E-mail',validators=[DataRequired(), Email()]) 
    subteam = SelectField("Subteam",validators=[DataRequired()],coerce=int)
    clas = SelectField("Class",validators=[DataRequired()],choices=class_choices)
    status = SelectField('Status',choices = status_choices,validators=[DataRequired()])
    major = SelectField('Major', choices=major_choices,
                        validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    submit_add_member = SubmitField("Add Member")

class AddCompetitionForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d')
    country = StringField("Country",validators=[DataRequired()])
    description = TextAreaField("Description",validators=[DataRequired()])
    reward = StringField("Reward",validators=[DataRequired()])
    submit_add_competition = SubmitField("Add Competition")
    #TODO:: COMPETITION'A LOGO EKLE

class AddSponsorForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    description = TextAreaField("Description",validators=[DataRequired()])
    field = StringField("Field",validators=[DataRequired()])
    country = StringField("Country",validators=[DataRequired()])
    address = TextAreaField("Address",validators=[DataRequired()])
    typ = SelectField("Type",coerce=int,validators=[DataRequired()])
    submit_add_sponsor = SubmitField("Add Sponsor")

class EditSponsorForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    description = TextAreaField("Description",validators=[DataRequired()])
    field = StringField("Field",validators=[DataRequired()])
    country = StringField("Country",validators=[DataRequired()])
    address = TextAreaField("Address",validators=[DataRequired()])
    typ = SelectField("Type",coerce=int,validators=[DataRequired()])
    submit_edit_sponsor = SubmitField("Update Sponsor")
    
class AddEquipmentForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    link = StringField("Link",validators=[DataRequired()])
    purchasedate = DateField("PurchaseDate",validators=[DataRequired()])
    available = BooleanField('Available')
    subteam = SelectField("Subteam",coerce=int,validators=[DataRequired()])
    submit_add_equipment = SubmitField("Add Equipment")
    picture = FileField(u'Picture')

class EditEquipmentForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    link = StringField("Link",validators=[DataRequired()])
    purchasedate = DateField("PurchaseDate",validators=[DataRequired()])
    available = BooleanField('Available')
    subteam = SelectField("Subteam",coerce=int,validators=[DataRequired()])
    submit_edit_equipment = SubmitField("Update Equipment")
    
class AddScheduleForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    deadline = DateField("Deadline",validators=[DataRequired()])
    done = BooleanField('Done')
    description = StringField("Description",validators=[DataRequired()])
    budget = StringField("Budget",validators=[DataRequired()])
    submit_add_schedule = SubmitField("Add Schedule")

class EditScheduleForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    deadline = DateField("Deadline",validators=[DataRequired()])
    done = BooleanField('Done')
    description = StringField("Description",validators=[DataRequired()])
    budget = StringField("Budget",validators=[DataRequired()])
    submit_edit_schedule = SubmitField("Update Schedule")
    

class AddDesignForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    year = StringField("Year",validators=[DataRequired()])
    maxspeed = StringField("Maxspeed",validators=[DataRequired()])
    weight = StringField("Weight",validators=[DataRequired()])
    duration = StringField("Duration",validators=[DataRequired()])
    is_autonomous = BooleanField("Is_Autonomous")
    typ = SelectField("Type",coerce=int,validators=[DataRequired()])
    submit_add_design = SubmitField("Add Design")

class EditDesignForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    year = StringField("Year",validators=[DataRequired()])
    maxspeed = StringField("Maxspeed",validators=[DataRequired()])
    weight = StringField("Weight",validators=[DataRequired()])
    duration = StringField("Duration",validators=[DataRequired()])
    is_autonomous = BooleanField("Is_Autonomous")
    typ = SelectField("Type",coerce=int,validators=[DataRequired()])
    submit_edit_design = SubmitField("Update Design")

class AddTutorialForm(FlaskForm):
    name = StringField('Tutorial Name',validators=[DataRequired()])
    area = StringField('Area')
    description = TextAreaField('Descrtiption')
    link = StringField('Link')
    isvideo = BooleanField('isVideo')

    submit_add_tutorial = SubmitField('Add Tutorial')

class EditTutorialForm(FlaskForm):
    name = StringField('Tutorial Name')
    area = StringField('Area')
    description = TextAreaField('Descrtiption')
    link = StringField('Link')
    isvideo = BooleanField('isVideo')

    submit_edit_tutorial = SubmitField('Update Tutorial')

class AddTeamLeaderForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    age = StringField("Age",validators=[DataRequired()])
    phone= StringField("Phone",validators=[DataRequired()])
    mail = EmailField('E-mail',validators=[DataRequired(), Email()]) 
    team = SelectField("Team",validators=[DataRequired()],coerce=int)
    clas = SelectField("Class",validators=[DataRequired()],choices=class_choices)
    status = SelectField('Status',choices = status_choices,validators=[DataRequired()])
    major = SelectField('Major', choices=major_choices,
                        validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    submit_add_team_leader = SubmitField("Add Team Leader")