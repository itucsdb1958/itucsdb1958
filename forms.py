from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, FloatField, SelectMultipleField, widgets, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SQLForm(FlaskForm):
    query = TextAreaField('SQL to be run', validators=[DataRequired()])
    submit = SubmitField('Run query')
