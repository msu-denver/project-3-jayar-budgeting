'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: __init__.py
Description: Budget Web App Initialization
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from flask import Flask
import os

app = Flask('Budgeting Web App')
# app.secret_key = os.environ['SECRET_KEY']
app.secret_key = 'you will never know'

# db initialization
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
db = SQLAlchemy(app)

# models initialization
# from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# cache setup
from flask_caching import Cache
cache = Cache()
cache.init_app(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes
print("Flask app instance created:", app)