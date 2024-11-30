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
    expenses = db.relationship('Expense', back_populates='user', cascade='all, delete-orphan')
    merchants = db.relationship('Merchant', back_populates='user', cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.id},{self.name}'

class CategoryType(db.Model):
    __tablename__ = 'category_types'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'
    
class PaymentType(db.Model):
    __tablename__ = 'payment_types'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __str__(self):
        return f'{self.code},{self.description}'
    
class ReceiptImage(db.Model):
    __tablename__ = 'receipt_images'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    expense = db.relationship('Expense', back_populates='receipt_image')

    def __str__(self):
        return f'{self.id},{self.user_id},{self.expense_id},{self.image},{self.name},{self.mimetype},{self.expense}'

class Merchant(db.Model):
    __tablename__ = 'merchants'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    reoccuring = db.Column(db.Boolean, nullable=False)
    user = db.relationship('User', back_populates='merchants')

    def __str__(self):
        return f'{self.id},{self.user_id},{self.reoccuring},{self.user}'

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    merchant = db.Column(db.Integer, db.ForeignKey('merchants.id'))
    category = db.Column(db.String, nullable=False)
    category_code = db.Column(db.Integer, db.ForeignKey('category_types.code'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_type = db.Column(db.String, nullable=False)
    payment_type_code = db.Column(db.Integer, db.ForeignKey('payment_types.code'))
    receipt_image = db.relationship('ReceiptImage', back_populates='expense', uselist=False, cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='expenses')

    def __str__(self):
        return f'{self.id},{self.user_id},{self.date},{self.merchant},{self.category},{self.category_code},{self.amount},{self.payment_type},{self.payment_type_code},{self.receipt_image},{self.user}'
    