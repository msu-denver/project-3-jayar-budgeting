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