'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: models.py
Description: Defines the models used for the budgeting web app that interacts with the PostgreSQL database
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)

    def __str__(self):
        return f'{self.id},{self.name}'