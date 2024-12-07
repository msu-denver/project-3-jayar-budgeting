import unittest
import requests
from bs4 import BeautifulSoup
import re

class ExpenseBudgetingTests(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    test_user = {
        "id": "testuser123",
        "name": "Test User",
        "passwd": "TestPass123!",
        "passwd_confirm": "TestPass123!"
    }
    
    def setUp(self):
        """Setup run before each test method"""
        self.session = requests.Session()
        
    def get_csrf_token(self, url):
        """Helper method to get CSRF token from form"""
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        return csrf_token
    
    def register_test_user(self):
        """Helper method to register a test user"""
        csrf_token = self.get_csrf_token(f"{self.BASE_URL}/signup")
        data = {
            'csrf_token': csrf_token,
            **self.test_user
        }
        return self.session.post(f"{self.BASE_URL}/signup", data=data)

    def login_test_user(self):
        """Helper method to login the test user"""
        csrf_token = self.get_csrf_token(f"{self.BASE_URL}/login")
        data = {
            'csrf_token': csrf_token,
            'id': self.test_user['id'],
            'passwd': self.test_user['passwd']
        }
        return self.session.post(f"{self.BASE_URL}/login", data=data)

    def test_1_user_registration(self):
        """Test user registration with valid and invalid data"""
        # Test successful registration
        response = self.register_test_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Account created successfully", response.text)

        # Test duplicate user registration
        response = self.register_test_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn("User ID already in use", response.text)

    def test_2_user_login(self):
        """Test user login functionality"""
        # Register user first if not exists
        self.register_test_user()
        
        # Test successful login
        response = self.login_test_user()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logged in successfully", response.text)
        
        # Test invalid password
        csrf_token = self.get_csrf_token(f"{self.BASE_URL}/login")
        login_data = {
            'csrf_token': csrf_token,
            'id': self.test_user['id'],
            'passwd': 'wrongpassword'
        }
        response = self.session.post(
            f"{self.BASE_URL}/login",
            data=login_data
        )
        self.assertIn("Invalid username or password", response.text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
