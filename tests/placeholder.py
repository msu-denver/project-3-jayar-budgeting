import unittest
import requests
from datetime import date, timedelta
import json

class ExpenseBudgetingTests(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    test_user = {
        "id": "testuser123",
        "name": "Test User",
        "passwd": "TestPass123!",
        "passwd_confirm": "TestPass123!"
    }
    
    def setUp(self):
        """Setup run before each test method"""
        self.session = requests.Session()
        self.token = None
        # Clean up any existing test user
        try:
            self.cleanup_test_user()
        except:
            pass

    def tearDown(self):
        """Cleanup after each test"""
        try:
            self.cleanup_test_user()
        except:
            pass

    def cleanup_test_user(self):
        """Helper method to remove test user if exists"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.session.delete(f"{self.BASE_URL}/api/users/{self.test_user['id']}", headers=headers)

    def test_1_user_registration(self):
        """Test user registration with valid and invalid data"""
        # Test successful registration
        response = self.session.post(
            f"{self.BASE_URL}/signup",
            data=self.test_user
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Account created successfully", response.text)

        # Test duplicate user registration
        response = self.session.post(
            f"{self.BASE_URL}/signup",
            data=self.test_user
        )
        self.assertIn("User ID already in use", response.text)

    def test_2_user_login(self):
        """Test user login functionality"""
        # Test successful login
        login_data = {
            "id": self.test_user["id"],
            "passwd": self.test_user["passwd"]
        }
        response = self.session.post(
            f"{self.BASE_URL}/login",
            data=login_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Logged in successfully", response.text)
        
        # Test invalid password
        login_data["passwd"] = "wrongpassword"
        response = self.session.post(
            f"{self.BASE_URL}/login",
            data=login_data
        )
        self.assertIn("Invalid username or password", response.text)

    def test_3_expense_operations(self):
        """Test expense creation, listing, and deletion"""
        # Login first
        self.session.post(
            f"{self.BASE_URL}/login",
            data={"id": self.test_user["id"], "passwd": self.test_user["passwd"]}
        )

        # Test expense creation
        expense_data = {
            "date": date.today().isoformat(),
            "merchant": "TEST STORE",
            "category": "1",  # Assuming 1 is a valid category code
            "amount": "50.25",
            "payment_type": "1"  # Assuming 1 is a valid payment type code
        }
        response = self.session.post(
            f"{self.BASE_URL}/create-expense",
            data=expense_data
        )
        self.assertIn("Expense created successfully", response.text)

        # Test expense listing
        response = self.session.get(f"{self.BASE_URL}/expenses/statement")
        self.assertEqual(response.status_code, 200)
        self.assertIn("TEST STORE", response.text)
        self.assertIn("50.25", response.text)

    def test_4_search_functionality(self):
        """Test expense search functionality"""
        # Login first
        self.session.post(
            f"{self.BASE_URL}/login",
            data={"id": self.test_user["id"], "passwd": self.test_user["passwd"]}
        )

        # Test search with various parameters
        search_params = {
            "date": date.today().isoformat(),
            "category": "1",
            "payment_type": "1"
        }
        response = self.session.get(
            f"{self.BASE_URL}/search",
            params=search_params
        )
        self.assertEqual(response.status_code, 200)

    def test_5_visualization(self):
        """Test expense visualization endpoint"""
        # Login first
        self.session.post(
            f"{self.BASE_URL}/login",
            data={"id": self.test_user["id"], "passwd": self.test_user["passwd"]}
        )

        response = self.session.get(f"{self.BASE_URL}/visualize")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image/png", response.headers["Content-Type"])

if __name__ == '__main__':
    unittest.main(verbosity=2)