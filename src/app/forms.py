'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: forms.py
Description: Defines the forms used in the budgeting web app to handle user input with Flask-WTF
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from datetime import date
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, SelectField, DecimalField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange
from app import db
from app.models import CategoryType, PaymentType

class SignUpForm(FlaskForm):
    id = StringField(
        'User ID', 
        validators=[
            DataRequired(message='You must enter a user ID.'), 
            Length(min=4, max=20)
        ]
    )
    name = StringField(
        'Name', 
        validators=[
            DataRequired(message='You must enter a name.'), 
            Length(max=50)
        ]
    )
    passwd = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='You must enter a password.'), 
            Length(min=6, message='Password must be at least 6 characters')
        ]
    )
    passwd_confirm = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(message='You must confirm your password.'), 
            EqualTo('passwd', message='Passwords must match')
        ]
    )
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField(
        'User ID', 
        validators=[
            DataRequired(), 
            Length(min=4, max=20)
        ]
    )
    passwd = PasswordField(
        'Password', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Login')

class CreateExpenseForm(FlaskForm):
    date = DateField(
        'Transaction Date',
        validators=[DataRequired(message='You must enter a date.')], 
        render_kw={"max": date.today().isoformat()}
    )
    merchant = StringField(
        'Merchant Name', 
        validators=[DataRequired(message='You must enter a merchant.')]
    )
    category = SelectField(
        'Category', 
        choices=[], 
        validators=[DataRequired(message='You must enter a category.')]
    )
    amount = DecimalField(
        'Amount Paid', 
        places=2, 
        rounding=None, 
        validators=[
            DataRequired(message='You must enter an amount.'), 
            NumberRange(min=0)
        ]
    )
    payment_type = SelectField(
        'Payment Method', 
        choices=[], 
        validators=[DataRequired(message='You must enter a payment type.')]                
    )
    receipt_image = FileField(
        'Upload Receipt (optional)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Please upload a jpg, jpeg, or png image.')]
    )
    submit = SubmitField('Create New Expense')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [
            (category_type.code, category_type.description) 
            for category_type in CategoryType.query.all()
        ]
        self.payment_type.choices = [
            (payment_type.code, payment_type.description) 
            for payment_type in PaymentType.query.all()
        ]

class DeleteExpenseForm(FlaskForm):
    expense_id = StringField(
        'Expense ID', 
        validators=[DataRequired()]
    )
    confirm = BooleanField(
        'I understand this action cannot be undone', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Delete Expense')

class SearchExpenseForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    category = SelectField('Category', choices=[], validators=[Optional()])
    payment_type = SelectField('Payment Method', choices=[], validators=[Optional()])
    charge_type = SelectField(
        'Charge Type',
        choices=[('', 'Select'), ('recurring', 'Recurring'), ('one-time', 'One-Time')],
        validators=[Optional()]
    )
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate dropdown choices from database
        self.category.choices = [('', 'Select a Category')] + [
            (str(cat.code), cat.name) for cat in db.session.query(CategoryType).all()
        ]
        self.payment_type.choices = [('', 'Select a Payment Method')] + [
            (str(pt.code), pt.name) for pt in db.session.query(PaymentType).all()
        ]

class ListExpenseForm(FlaskForm):
    page = IntegerField('Page', default=1, validators=[Optional(), NumberRange(min=1, message="Page must be 1 or greater.")])
    items_per_page = IntegerField('Items Per Page', default=10, validators=[Optional(), NumberRange(min=1, max=100, message="Items per page must be between 1 and 100.")])
    submit = SubmitField('Go')