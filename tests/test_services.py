'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: test_services.py
Description: White-Box test for main methods in ExpenseService class in expense_service.py
Authors: Alexander Gonzalez Ramirez
'''

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, db, TestConfig
from app.models import Expense, Merchant, User, CategoryType, PaymentType
from app.expense_service import ExpenseService


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        app.config.from_object('app.TestConfig')
        self.app = app.test_client()

        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        self.user = User(id="123", name="test_user", passwd=b"password123")
        db.session.add(self.user)
        db.session.commit()

        self.service = ExpenseService(db, self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_get_or_create_merchant_creates_new(self):
        # Ensure no merchant exists initially
        self.assertIsNone(Merchant.query.filter_by(id="TestMerchant").first())

        merchant = self.service.get_or_create_merchant("TestMerchant")
        self.assertIsNotNone(merchant)
        self.assertEqual(merchant.id, "TestMerchant")
        self.assertFalse(merchant.reoccuring)

    def test_get_or_create_merchant_retrieves_existing(self):
        # Add an existing merchant
        merchant = Merchant(id="TestMerchant", user_id=self.user.id, reoccuring=False, user=self.user)
        db.session.add(merchant)
        db.session.commit()

        retrieved_merchant = self.service.get_or_create_merchant("TestMerchant")
        self.assertEqual(retrieved_merchant.id, "TestMerchant")
        self.assertTrue(retrieved_merchant.reoccuring)

    def test_create_expense(self):
        # Merchant entry
        merchant = Merchant(id="TestMerchant", user_id=self.user.id, reoccuring=False, user=self.user)
        db.session.add(merchant)

        # Category type entry
        category_type = CategoryType(code=1, description="Food")
        db.session.add(category_type)
        db.session.commit()

        # Payment type entry
        payment_type = PaymentType(code=2, description="Credit Card")
        db.session.add(payment_type)
        db.session.commit()

        # Create data objects
        form = type('Form', (object,), {'data': {'date': "2024-12-06", 'amount': 100.00}})
        category = type('Category', (object,), {'description': "Food", 'code': 1})
        payment_type = type('PaymentType', (object,), {'description': "Credit Card", 'code': 2})

        
        expense = self.service.create_expense(
            form=form,
            merchant_name="TestMerchant",
            category=category,
            payment_type=payment_type,
            current_user=self.user
        )

        self.assertIsNotNone(expense)
        self.assertEqual(expense.user_id, self.user.id)
        self.assertEqual(expense.date.isoformat(), "2024-12-06")
        self.assertEqual(expense.merchant, "TestMerchant")
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.category_code, 1)
        self.assertEqual(expense.amount, 100.00)
        self.assertEqual(expense.payment_type, "Credit Card")
        self.assertEqual(expense.payment_type_code, 2)

    def test_check_merchant_updates_merchant(self):
        # Add merchant and two expenses
        merchant = Merchant(id="TestMerchant", user_id=self.user.id, reoccuring=True)
        expense1 = Expense(
            user_id=self.user.id,
            date="2024-12-06",
            merchant="TestMerchant",
            category="Food",
            category_code=1,
            amount=50.00,
            payment_type="Credit Card",
            payment_type_code=2
        )
        expense2 = Expense(
            user_id=self.user.id,
            date="2024-12-07",
            merchant="TestMerchant",
            category="Travel",
            category_code=2,
            amount=100.00,
            payment_type="Cash",
            payment_type_code=1
        )
        db.session.add_all([merchant, expense1, expense2])
        db.session.commit()

        self.service.check_merchant(id=expense1.id)
        updated_merchant = Merchant.query.filter_by(id="TestMerchant").first()
        self.assertFalse(updated_merchant.reoccuring)

if __name__ == "__main__":
    unittest.main()