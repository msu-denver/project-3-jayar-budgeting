"""
CS3250 - Software Development Methods and Tools - Final Project
Module Name: routes.py
Description: Defines the web routes for the budgeting web app including URL mappings and the associated view functions
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
"""

import bcrypt
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user
from app import app, db
from app.models import User, Expense, CategoryType, PaymentType, Merchant, ReceiptImage
from app.forms import SignUpForm, LoginForm, DeleteExpenseForm, SearchExpenseForm, ListExpenseForm, CreateExpenseForm
from service.expense_service import ExpenseService
from sqlalchemy import func


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Web app routes
@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Handle the new user data
        new_user_passwd = bcrypt.hashpw(
            form.passwd.data.encode('utf-8'), 
            bcrypt.gensalt()
        )
        new_user = User(
            id=form.id.data, 
            name=form.name.data, 
            passwd=new_user_passwd
        )
        # Ensure unique user ID before committing
        existing_user = User.query.filter_by(id=form.id.data).first()
        if not existing_user:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully.', 'successful')
            return redirect(url_for('index'))
        else:
            flash('User ID already in use.', 'error')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            session['user_id'] = user.id
            flash('Logged in successfully.', 'successful')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Logged out successfully.', 'successful')
    return redirect(url_for('login'))


@app.route('/create-expense', methods=['GET', 'POST'])
@login_required
def create_expense():
    form = CreateExpenseForm()
    service = ExpenseService(db, current_user)
    if form.validate_on_submit():
        try:
            # Handle Merchant Data
            merchant_name = form.merchant.data.strip().upper()
            merchant = service.get_or_create_merchant(merchant_name)

            # Create Expense Record
            category = CategoryType.query.get(form.category.data)
            payment_type = PaymentType.query.get(form.payment_type.data)
            new_expense = service.create_expense(form, merchant_name, category, payment_type, current_user)
            
            # Handle Receipt Image
            receipt = form.receipt_image.data
            if receipt:
                service.create_image(receipt, new_expense)
            flash('Expense created successfully!', 'successful')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating expense: {str(e)}', 'error')
    return render_template('create_expense.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_expenses():
    form = SearchExpenseForm()
    expenses = []

    if request.method == 'POST' and form.validate_on_submit():
        query = db.session.query(Expense)
        
        if form.date.data:
            query = query.filter(Expense.date == form.date.data)

        if form.category.data:
            query = query.filter(Expense.category_code == int(form.category.data))
        
        if form.payment_type.data:
            query = query.filter(Expense.payment_type_code == int(form.payment_type.data))
        
        if form.charge_type.data:
            is_recurring = form.charge_type.data == 'recurring'
            query = query.filter(Expense.is_recurring == is_recurring)

        expenses = query.all()

    return render_template('search.html', form=form, expenses=expenses)


@app.route('/expenses', methods=['GET'])
@login_required
def list_expenses():
    form = ListExpenseForm(request.args)
    
    if not form.validate():
        # If form validation fails, default to first page with 10 items
        page = 1
        items_per_page = 10
    else:
        page = form.page.data
        items_per_page = form.items_per_page.data

    # Use Flask-SQLAlchemy's pagination
    expenses = Expense.query.filter_by(user_id=session['user_id']) \
        .order_by(Expense.date.desc()) \
        .paginate(page=page, per_page=items_per_page, error_out=False)
    
    return render_template('list_expenses.html', expenses=expenses, form=form)


@app.route('/delete_expense', methods=['GET', 'POST'])
@login_required
def delete_expense():
    form = DeleteExpenseForm()
    expense = None
    if form.validate_on_submit():
        if form.confirm.data:
            expense = Expense.query.get_or_404(form.data.expense_id)
    
            # Check if the expense belongs to the logged-in user
            if expense.user_id != session['user_id']:
                flash('You do not have permission to delete this expense.', 'error')
                return redirect(url_for('index'))
            
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


@app.route('/expenses/statement', methods=['GET'])
@login_required
def expenses_statement():
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    
    # Fetch user's expenses
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc())\
        .paginate(page=page, per_page=items_per_page, error_out=False)
    
    # Calculate summary data
    total_spent = db.session.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == current_user.id).scalar() or 0
    total_by_payment = db.session.query(Expense.payment_type, func.sum(Expense.amount))\
        .filter(Expense.user_id == current_user.id)\
        .group_by(Expense.payment_type).all()
    
    return render_template(
        'statement.html', 
        expenses=expenses, 
        total_spent=total_spent, 
        total_by_payment=total_by_payment,
        page=page,
        items_per_page=items_per_page
    )


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500