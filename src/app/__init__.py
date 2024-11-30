'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: __init__.py
Description: Budget Web App Initialization
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask('Budgeting Web App')
app.secret_key = 'you will never know'

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI','postgresql://postgres:postgres1234@localhost:5432/budgeting')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes
from app.db_init import initialize_database, populate_database
from app.models import User

# database initialization
initialize_database()
populate_database()

# models initialization
with app.app_context(): 
    db.create_all()

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

print("Flask app instance created:", app)