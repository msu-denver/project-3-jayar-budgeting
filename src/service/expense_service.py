'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: expense_service.py
Description: Defines the services used in new expense creations
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from werkzeug.utils import secure_filename
from app.models import Expense, Merchant, ReceiptImage
from app import db


class ExpenseService:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def get_or_create_merchant(self, merchant_name):
        merchant = Merchant.query.filter_by(id=merchant_name).first()
        if not merchant:
            merchant = Merchant(
                id=merchant_name,
                user_id=self.user.id,
                reoccuring=False,
                user=self.user
            )
            self.db.session.add(merchant)
            self.db.session.commit()
        else:
            merchant.reoccuring = True
        return merchant

    def create_image(self, receipt, expense):
        receipt_filename = secure_filename(receipt.filename)
        receipt_data = receipt.read()
        new_receipt = ReceiptImage(
            user_id=self.user.id,
            expense_id=expense.id,
            image=receipt_data,
            name=receipt_filename,
            mimetype=receipt.mimetype,
            expense=expense
        )
        self.db.session.add(new_receipt)
        self.db.session.commit()
        return new_receipt
    
    def create_expense(self, form, merchant_name, category, payment_type, current_user):
        new_expense = Expense(
            user_id=current_user.id,
            date=form.data['date'],
            merchant=merchant_name,
            category=category.description,
            category_code=category.code,
            amount=form.data['amount'],
            payment_type=payment_type.description,
            payment_type_code=payment_type.code,
            user=current_user
        )
        db.session.add(new_expense)
        db.session.commit()
        return new_expense