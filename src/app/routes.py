'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: routes.py
Description: Defines the web routes for the budgeting web app including URL mappings and the associated view functions
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from app import app, db
from app.models import User
from app.forms import SignUpForm
from flask import render_template, request, redirect, url_for, flash
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            hashed_passwd = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=form.id.data, name=form.name.data, passwd=hashed_passwd)
            existing_user = User.query.filter_by(id=form.id.data).first()
            if existing_user:
                flash('User ID already in use.', 'error')
                print('User ID not created due to existing ID')
            else:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully.', 'successful')
                print(f'Account created: {form.id.data}')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)