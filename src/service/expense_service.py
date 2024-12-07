'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: expense_service.py
Description: Defines the services used in new expense creations
Authors: Yedani Mendoza Gurrola, Artem Marsh, Jose Gomez Betancourt, Alexander Gonzalez Ramirez, Rhodes Ferris
'''

from werkzeug.utils import secure_filename

from app import db
from app.models import Expense, Merchant, ReceiptImage


class ExpenseService:
    """A service class for managing expenses, merchants, and receipt images."""

    def __init__(self, db, user):
        """Initializes the ExpenseService class with a database session and user."""
        self.db = db
        self.user = user

    def get_or_create_merchant(self, merchant_name):
        """Retrieves an existing merchant by name or creates a new one if not found."""
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
        """Creates a new receipt image associated with a specific expense."""
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
        """Creates a new expense entry in the database."""
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
    
    def check_merchant(self, id):
        """Checks if a merchant associated with an expense should be updated or deleted if there are no related expenses."""
        # Fetch the expense by ID and ensure it belongs to the current user
        expense = Expense.query.filter(
            Expense.id == id, 
            Expense.user_id == self.user.id
        ).first()
        
        if expense and expense.merchant_rel:
            expense_merchant = expense.merchant_rel
            
            # Count how many expenses are linked to this merchant
            total_expenses = Expense.query.filter_by(
                user_id=self.user.id, 
                merchant=expense_merchant.id
            ).count()

            if total_expenses - 1 == 1:
                # If only one other expense is left, update the merchant as non-recurring
                expense_merchant.reoccuring = False
            elif total_expenses - 1 == 0:
                # If no other expenses remain, delete the merchant
                try:
                    self.db.session.delete(expense_merchant)
                    self.db.session.commit()
                    print('Merchant deleted successfully.')
                except Exception as e:
                    self.db.session.rollback()
                    print(f"Error deleting merchant: {str(e)}")
