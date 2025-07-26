"""Test data management utilities."""

import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LoginCredentials:
    """Data class for login credentials."""
    username: str
    password: str
    expected_result: str = "success"  # "success" or "failure"
    expected_error: str = ""


@dataclass
class UserData:
    """Data class for test user information."""
    username: str
    password: str
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    role: str = "user"


class DataManager:
    """Manager class for test data operations."""
    
    def __init__(self, data_file_path: str = "utils/test_data.json"):
        """Initialize test data manager.
        
        Args:
            data_file_path: Path to the test data JSON file
        """
        self.data_file_path = data_file_path
        self._ensure_data_file_exists()
        
    def _ensure_data_file_exists(self) -> None:
        """Ensure the test data file exists, create if not."""
        if not os.path.exists(self.data_file_path):
            os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
            self._create_default_data_file()
            
    def _create_default_data_file(self) -> None:
        """Create default test data file."""
        default_data = {
            "valid_users": [
                {
                    "username": "student",
                    "password": "Password123",
                    "email": "student@test.com",
                    "role": "student"
                }
            ],
            "invalid_credentials": [
                {
                    "username": "incorrectUser",
                    "password": "Password123",
                    "expected_error": "Your username is invalid!"
                },
                {
                    "username": "student",
                    "password": "incorrectPassword",
                    "expected_error": "Your password is invalid!"
                },
                {
                    "username": "",
                    "password": "Password123",
                    "expected_error": "Your username is invalid!"
                },
                {
                    "username": "student",
                    "password": "",
                    "expected_error": "Your password is invalid!"
                }
            ],
            "test_scenarios": {
                "boundary_testing": {
                    "max_length_username": "a" * 255,
                    "max_length_password": "b" * 255,
                    "special_characters": "!@#$%^&*()_+-=[]{}|;:,.<>?"
                },
                "sql_injection": {
                    "username": "admin'; DROP TABLE users; --",
                    "password": "password"
                },
                "xss_testing": {
                    "username": "<script>alert('XSS')</script>",
                    "password": "password"
                }
            }
        }
        
        with open(self.data_file_path, 'w') as f:
            json.dump(default_data, f, indent=2)
            
    def load_test_data(self) -> Dict[str, Any]:
        """Load test data from JSON file.
        
        Returns:
            Dictionary containing test data
        """
        try:
            with open(self.data_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading test data: {e}")
            return {}
            
    def get_valid_credentials(self) -> List[LoginCredentials]:
        """Get list of valid login credentials.
        
        Returns:
            List of LoginCredentials objects
        """
        data = self.load_test_data()
        valid_users = data.get("valid_users", [])
        
        return [
            LoginCredentials(
                username=user["username"],
                password=user["password"],
                expected_result="success"
            )
            for user in valid_users
        ]
        
    def get_invalid_credentials(self) -> List[LoginCredentials]:
        """Get list of invalid login credentials.
        
        Returns:
            List of LoginCredentials objects
        """
        data = self.load_test_data()
        invalid_creds = data.get("invalid_credentials", [])
        
        return [
            LoginCredentials(
                username=cred["username"],
                password=cred["password"],
                expected_result="failure",
                expected_error=cred["expected_error"]
            )
            for cred in invalid_creds
        ]
        
    def get_boundary_test_data(self) -> Dict[str, str]:
        """Get boundary testing data.
        
        Returns:
            Dictionary with boundary test data
        """
        data = self.load_test_data()
        return data.get("test_scenarios", {}).get("boundary_testing", {})
        
    def get_security_test_data(self) -> Dict[str, Dict[str, str]]:
        """Get security testing data (SQL injection, XSS, etc.).
        
        Returns:
            Dictionary with security test data
        """
        data = self.load_test_data()
        scenarios = data.get("test_scenarios", {})
        return {
            "sql_injection": scenarios.get("sql_injection", {}),
            "xss_testing": scenarios.get("xss_testing", {})
        }
        
    def add_test_user(self, user: UserData) -> None:
        """Add a new test user to the data file.

        Args:
            user: UserData object to add
        """
        data = self.load_test_data()
        if "valid_users" not in data:
            data["valid_users"] = []
            
        user_dict = {
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
        
        data["valid_users"].append(user_dict)
        
        with open(self.data_file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def generate_random_credentials(self) -> LoginCredentials:
        """Generate random credentials for testing.
        
        Returns:
            LoginCredentials object with random data
        """
        import random
        import string
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        
        return LoginCredentials(
            username=f"testuser_{timestamp}_{random_suffix}",
            password=f"TestPass_{timestamp}",
            expected_result="failure",
            expected_error="Your username is invalid!"
        )


# Utility functions
def create_test_credentials(username: str, password: str, expected_result: str = "success", 
                          expected_error: str = "") -> LoginCredentials:
    """Create LoginCredentials object.
    
    Args:
        username: Username
        password: Password
        expected_result: Expected result ("success" or "failure")
        expected_error: Expected error message if failure
        
    Returns:
        LoginCredentials object
    """
    return LoginCredentials(
        username=username,
        password=password,
        expected_result=expected_result,
        expected_error=expected_error
    )


def get_default_valid_credentials() -> LoginCredentials:
    """Get default valid credentials.
    
    Returns:
        LoginCredentials object with default valid credentials
    """
    return LoginCredentials(
        username="student",
        password="Password123",
        expected_result="success"
    )


def get_empty_credentials() -> LoginCredentials:
    """Get empty credentials for testing.
    
    Returns:
        LoginCredentials object with empty values
    """
    return LoginCredentials(
        username="",
        password="",
        expected_result="failure",
        expected_error="Your username is invalid!"
    )


def validate_credentials_format(credentials: LoginCredentials) -> bool:
    """Validate credentials format.
    
    Args:
        credentials: LoginCredentials object to validate
        
    Returns:
        True if format is valid, False otherwise
    """
    if not isinstance(credentials.username, str) or not isinstance(credentials.password, str):
        return False
        
    if credentials.expected_result not in ["success", "failure"]:
        return False
        
    return True


# Test data constants
DEFAULT_TIMEOUT = 30000
ELEMENT_TIMEOUT = 10000
SHORT_TIMEOUT = 5000

# Common test messages
ERROR_MESSAGES = {
    "INVALID_USERNAME": "Your username is invalid!",
    "INVALID_PASSWORD": "Your password is invalid!",
    "LOGIN_FAILED": "Login failed",
    "PAGE_NOT_LOADED": "Page did not load correctly"
}

# Expected page elements
EXPECTED_ELEMENTS = {
    "LOGIN_PAGE": {
        "username_input": "#username",
        "password_input": "#password",
        "submit_button": "#submit",
        "error_message": "#error"
    },
    "DASHBOARD_PAGE": {
        "heading": "h1",
        "success_message": ".post-title",
        "logout_button": "a[href*='logout']"
    }
}
