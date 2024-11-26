'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: routes.py
Description: Defines the web routes for the budgeting web app including URL mappings and the associated view functions
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from app import app, db
from app.models import User, Expense
from app.forms import SignUpForm, LoginForm, DeleteExpenseForm
from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps
import bcrypt

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Logged in successfully.', 'successful')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logged out successfully.', 'successful')
    return redirect(url_for('login'))

@app.route('/delete_expense/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_expense(id):
    form = DeleteExpenseForm()
    expense = Expense.query.get_or_404(id)
    
    # Check if the expense belongs to the logged-in user
    if expense.user_id != session['user_id']:
        flash('You do not have permission to delete this expense.', 'error')
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        if form.confirm.data:
            try:
                db.session.delete(expense)
                db.session.commit()
                flash('Expense deleted successfully.', 'successful')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while deleting the expense.', 'error')
                print(f"Error deleting expense: {str(e)}")
        else:
            flash('Please confirm deletion by checking the box.', 'error')
    
    return render_template('delete.html', form=form, expense=expense)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    return render_template('signup.html', form=form)
