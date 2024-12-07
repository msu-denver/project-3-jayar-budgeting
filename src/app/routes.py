"""
CS3250 - Software Development Methods and Tools - Final Project
Module Name: routes.py
Description: Defines the web routes for the budgeting web app including URL mappings and the associated view functions
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
"""

import base64
from functools import wraps
from io import BytesIO

import bcrypt
import matplotlib.pyplot as plt
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, current_user, logout_user
from sqlalchemy import func

from app import app, db
from app.models import User, Expense, CategoryType, PaymentType, Merchant, ReceiptImage
from app.forms import SignUpForm, LoginForm, DeleteExpenseForm, SearchExpenseForm, CreateExpenseForm
from service.expense_service import ExpenseService


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            # Hash the user's password
            new_user_passwd = bcrypt.hashpw(
                form.passwd.data.encode('utf-8'),
                bcrypt.gensalt()
            )

            # Check if the user ID already exists
            existing_user = User.query.filter_by(id=form.id.data).first()
            if existing_user:
                flash('User ID already in use.', 'error')
                return redirect(url_for('signup'))
            
            # Create and add the new user
            new_user = User(
                id=form.id.data,
                name=form.name.data,
                passwd=new_user_passwd
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully.', 'successful')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the account. Please try again.', 'error')
            print(f"Error: {e}")
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect user to the home page if already logged in
    if 'user_id' in session:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Check if the user exists and the password matches
            user = User.query.filter_by(id=form.id.data).first()
            if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
                login_user(user)
                session['user_id'] = user.id
                flash('Logged in successfully.', 'successful')
                return redirect(url_for('home'))
            else:
                # Display error if the credentials are invalid
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            flash('An unexpected error occurred. Please try again.', 'error')
            print(f"Error: {e}")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        session.pop('user_id', None)
        session.pop('user_name', None)
        flash('Logged out successfully.', 'successful')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred while logging out. Please try again.', 'error')
        print(f"Error: {e}")
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')


@app.route('/create-expense', methods=['GET', 'POST'])
@login_required
def create_expense():
    form = CreateExpenseForm()
    service = ExpenseService(db, current_user)
    if form.validate_on_submit():
        try:
            # Format merchant name and check if it exists
            merchant_name = form.merchant.data.strip().upper()
            merchant = service.get_or_create_merchant(merchant_name)

            # Create Expense entry
            category = CategoryType.query.get(form.category.data)
            payment_type = PaymentType.query.get(form.payment_type.data)
            new_expense = service.create_expense(form, merchant_name, category, payment_type, current_user)
            
            # Create new receipt image if submitted
            receipt = form.receipt_image.data
            if receipt:
                service.create_image(receipt, new_expense)
            flash('Expense created successfully!', 'successful')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('An unexpected error occurred while adding expense. Please try again.', 'error')
            return redirect(url_for('create_expense'))
    return render_template('create_expense.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_expenses():
    form = SearchExpenseForm()
    # Collect search params pass to the list route
    if request.method == 'POST':
        query = {}
        if form.date.data:
            query['date'] = form.date.data
        if form.category.data:
            query['category'] = form.category.data
        if form.payment_type.data:
            query['payment_type'] = form.payment_type.data
        if form.charge_type.data:
            query['charge_type'] = form.charge_type.data
        return redirect(url_for('list_expenses', **query))
    return render_template('search.html', form=form)

@app.route('/expenses', methods=['GET'])
@login_required
def list_expenses():
    # Fetch the parameters sent from the search route
    date = request.args.get('date')
    category = request.args.get('category') 
    payment_type = request.args.get('payment_type') 
    charge_type = request.args.get('charge_type') 

    # Filter the users expenses to match the parameters chosen
    query = Expense.query.filter_by(user_id=session['user_id'])
    if date:
        query = query.filter(Expense.date == date)
    if category:
        query = query.filter(Expense.category_code == int(category))
    if payment_type:
        query = query.filter(Expense.payment_type_code == int(payment_type))
    if charge_type:
        is_recurring = charge_type == 'reocurring'
        query = query.join(Merchant).filter(Merchant.reoccuring == is_recurring)

    # Order expenses by most recent and paginate results with Flask-SQLAlchemy's pagination
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)
    expenses = query.order_by(Expense.date.desc()).paginate(page=page, per_page=items_per_page, error_out=False)

    return render_template(
        'list_expenses.html', 
        expenses=expenses, 
        page=page,
        items_per_page=items_per_page
    )


@app.route('/delete_expense', methods=['GET', 'POST'])
@login_required
def delete_expense():
    form = DeleteExpenseForm()
    service = ExpenseService(db, current_user)
    expense = None
    if form.validate_on_submit():
        if form.confirm.data:
            # Check that the expense exists and belongs to the logged-in user
            expense = Expense.query.get(form.data['expense_id'])
            if not expense:
                flash(f'Expense does not exist.', 'error')
                return redirect(url_for('delete_expense'))
            if expense.user_id != session['user_id']:
                flash('You do not have permission to delete this expense.', 'error')
                return redirect(url_for('index'))
            
            # Delete the expense from the database if expense exists and belongs to the logged-in user
            try:
                service.check_merchant(form.data['expense_id'])
                db.session.delete(expense)
                db.session.commit()
                flash('Expense deleted successfully.', 'successful')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while deleting the expense.', 'error')
                print(f"Error deleting expense: {str(e)}")
    return render_template('delete.html', form=form, expense=expense)


@app.route('/expenses/statement', methods=['GET'])
@login_required
def expenses_statement():
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 10, type=int)

    # Fetch user's expenses
    expenses = Expense.query.filter_by(user_id=current_user.id) \
        .order_by(Expense.date.desc()) \
        .paginate(page=page, per_page=items_per_page, error_out=False)

    # Calculate summary data
    total_spent = db.session.query(func.sum(Expense.amount)) \
        .filter(Expense.user_id == current_user.id).scalar() or 0
    total_by_payment = db.session.query(Expense.payment_type, func.sum(Expense.amount)) \
        .filter(Expense.user_id == current_user.id) \
        .group_by(Expense.payment_type).all()

    return render_template('statement.html',
                           expenses=expenses,
                           total_spent=total_spent,
                           total_by_payment=total_by_payment,
                           page=page,
                           items_per_page=items_per_page)


@app.route('/visualize', methods=['GET'])
@login_required
def visualize_expenses():
    # Fetch expenses grouped by category
    query = db.session.query(
        CategoryType.description,
        func.count(Expense.id).label('count')
    ).join(Expense, Expense.category_code == CategoryType.code) \
     .filter(Expense.user_id == session['user_id']) \
     .group_by(CategoryType.description).all()

    # Prepare data for the graph
    categories = [row[0] for row in query]
    counts = [row[1] for row in query]

    # Generate the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color='blue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Expenses')
    plt.xticks(rotation=45)

    # Save the graph to a string buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image in base64
    graph = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return render_template('visualization.html', graph=graph)

@app.route('/expense/<int:id>/receipt_image')
def get_receipt_image(id):
    # Check if the expense has a receipt image to display
    expense = Expense.query.get_or_404(id)
    if expense.receipt_image:
        receipt = expense.receipt_image
        return render_template(
            'view_image.html',
            expense=expense,
            receipt_image=f"data:{receipt.mimetype};base64,{base64.b64encode(receipt.image).decode('utf-8')}"
        )
    else:
        abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
