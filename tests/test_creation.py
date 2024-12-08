'''
CS3250 - Software Development Methods and Tools - Final Project
Module Name: test_creation.py
Description: Black-Box test for creating expense
Authors: Artem Marsh
'''

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class ExpenseBudgetingTests(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.browser, 10)
        self.browser.get('http://127.0.0.1:5000')

    def tearDown(self):
        self.browser.quit()

    def test_user_login(self):
        self.browser.get('http://127.0.0.1:5000/login')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

        user_id = self.browser.find_element(By.ID, 'id')
        password = self.browser.find_element(By.ID, 'passwd')

        user_id.send_keys('testuser123')
        password.send_keys('TestPass123!')

        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary[type="submit"]')
        submit_button.click()

        welcome_message = self.wait.until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertEqual(welcome_message.text, "Welcome, TestUser!")
    
    def test_create_expense(self):
        # First login
        self.test_user_login()
        
        # Navigate to create expense page
        add_new = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Add New"))
        )
        add_new.click()

        # Wait for form to load
        self.wait.until(EC.presence_of_element_located((By.ID, 'date')))

        # Fill in expense form
        date_input = self.browser.find_element(By.ID, 'date')
        merchant = self.browser.find_element(By.ID, 'merchant')
        category = Select(self.browser.find_element(By.ID, 'category'))
        amount = self.browser.find_element(By.ID, 'amount')
        payment_type = Select(self.browser.find_element(By.ID, 'payment_type'))

        # Use JavaScript to set date value
        self.browser.execute_script("arguments[0].value = '2024-03-07'", date_input)
        merchant.send_keys('Test Store')
        category.select_by_visible_text('Food and Groceries')
        amount.send_keys('50.00')
        payment_type.select_by_visible_text('Credit/Debit Card')

        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary[type="submit"]')
        submit_button.click()

        welcome_message = self.wait.until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        self.assertEqual(welcome_message.text, "Welcome, TestUser!")

if __name__ == '__main__':
    unittest.main()
