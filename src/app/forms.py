'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: forms.py
Description: Defines the forms used in the budgeting web app to handle user input with Flask-WTF
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from flask_wtf import FlaskForm
from wtforms import *
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange

class SignUpForm(FlaskForm):
    id = StringField('User ID', validators=[DataRequired(), Length(min=4, max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    passwd = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters')])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('passwd', message='Passwords must match')])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('User ID', validators=[DataRequired(), Length(min=4, max=20)])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DeleteExpenseForm(FlaskForm):
    expense_id = StringField('Expense ID', validators=[DataRequired()])
    confirm = BooleanField('I understand this action cannot be undone', validators=[DataRequired()])
    submit = SubmitField('Delete Expense')
