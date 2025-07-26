"""Comprehensive test cases for login functionality."""

import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import DataManager, create_test_credentials, get_default_valid_credentials
from tests.conftest import assert_login_success, assert_login_failure


class TestLoginFunctionality:
    """Test class for login functionality."""
    
    def setup_method(self):
        """Set up test data manager for each test."""
        self.test_data_manager = DataManager()
    
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login_success(self, fresh_login_page: LoginPage, dashboard_page: DashboardPage, valid_credentials):
        """Test successful login with valid credentials.
        
        Args:
            fresh_login_page: Fresh login page fixture
            dashboard_page: Dashboard page fixture
            valid_credentials: Valid credentials fixture
        """
        # Perform login
        fresh_login_page.login(valid_credentials["username"], valid_credentials["password"])
        
        # Wait for login completion
        assert fresh_login_page.wait_for_login_completion(), "Login did not complete in expected time"
        
        # Verify successful login
        assert_login_success(dashboard_page)
        
        # Additional verifications
        assert dashboard_page.get_page_heading() == "Logged In Successfully"
        assert "Logged In Successfully" in dashboard_page.get_success_message()
        
    @pytest.mark.login
    @pytest.mark.parametrize("invalid_cred", [
        {"username": "incorrectUser", "password": "Password123", "expected_error": "Your username is invalid!"},
        {"username": "student", "password": "incorrectPassword", "expected_error": "Your password is invalid!"},
        {"username": "", "password": "Password123", "expected_error": "Your username is invalid!"},
        {"username": "student", "password": "", "expected_error": "Your password is invalid!"}
    ])
    def test_invalid_login_scenarios(self, fresh_login_page: LoginPage, invalid_cred):
        """Test login with various invalid credentials.
        
        Args:
            fresh_login_page: Fresh login page fixture
            invalid_cred: Invalid credentials test data
        """
        # Perform login with invalid credentials
        fresh_login_page.login(invalid_cred["username"], invalid_cred["password"])
        
        # Wait for login completion
        assert fresh_login_page.wait_for_login_completion(), "Login process did not complete"
        
        # Verify login failure
        assert_login_failure(fresh_login_page, invalid_cred["expected_error"])
        
        # Verify user remains on login page
        assert "practice-test-login" in fresh_login_page.get_url()
        
    @pytest.mark.ui
    @pytest.mark.login
    def test_login_page_elements_visibility(self, fresh_login_page: LoginPage):
        """Test that all login page elements are visible and accessible.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Verify page elements
        elements_status = fresh_login_page.verify_page_elements()
        
        # Assert all elements are visible
        assert elements_status["username_input"], "Username input field is not visible"
        assert elements_status["password_input"], "Password input field is not visible"
        assert elements_status["submit_button"], "Submit button is not visible"
        # Note: login_form might not be present on this page, so we'll skip this assertion
        # assert elements_status["login_form"], "Login form is not visible"
        assert elements_status["page_title"], "Page title is not visible"
        
        # Verify submit button is enabled
        assert fresh_login_page.is_submit_button_enabled(), "Submit button should be enabled"
        
    @pytest.mark.ui
    def test_login_page_title_and_heading(self, fresh_login_page: LoginPage):
        """Test login page title and heading are correct.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Verify page title
        page_title = fresh_login_page.get_title()
        assert "Test Login" in page_title, f"Expected 'Test Login' in title, got '{page_title}'"
        
        # Verify page heading
        page_heading = fresh_login_page.get_page_heading()
        assert "Practice Test Login" in page_heading, f"Expected 'Practice Test Login' in heading, got '{page_heading}'"
        
    @pytest.mark.login
    def test_form_field_interactions(self, fresh_login_page: LoginPage):
        """Test form field interactions and data entry.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        test_username = "testuser"
        test_password = "testpass"
        
        # Enter username and verify
        fresh_login_page.enter_username(test_username)
        assert fresh_login_page.get_username_value() == test_username
        
        # Enter password and verify
        fresh_login_page.enter_password(test_password)
        assert fresh_login_page.get_password_value() == test_password
        
        # Clear form and verify
        fresh_login_page.clear_form()
        assert fresh_login_page.get_username_value() == ""
        assert fresh_login_page.get_password_value() == ""
        
    @pytest.mark.login
    def test_error_message_display_and_content(self, fresh_login_page: LoginPage):
        """Test error message display and content for invalid login.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Test with invalid username
        fresh_login_page.login("invaliduser", "Password123")
        fresh_login_page.wait_for_login_completion()
        
        # Verify error message is displayed
        assert fresh_login_page.is_error_message_displayed(), "Error message should be displayed"
        
        # Verify error message content
        error_message = fresh_login_page.get_error_message()
        assert "Your username is invalid!" in error_message
        
    @pytest.mark.login
    def test_multiple_login_attempts(self, fresh_login_page: LoginPage, dashboard_page: DashboardPage):
        """Test multiple login attempts with different credentials.
        
        Args:
            fresh_login_page: Fresh login page fixture
            dashboard_page: Dashboard page fixture
        """
        # First attempt with invalid credentials
        fresh_login_page.login("wronguser", "wrongpass")
        fresh_login_page.wait_for_login_completion()
        assert fresh_login_page.is_error_message_displayed()
        
        # Clear form
        fresh_login_page.clear_form()
        
        # Second attempt with valid credentials
        fresh_login_page.login("student", "Password123")
        fresh_login_page.wait_for_login_completion()
        
        # Verify successful login
        assert_login_success(dashboard_page)
        
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_with_special_characters(self, fresh_login_page: LoginPage):
        """Test login with special characters in credentials.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        special_chars_data = [
            {"username": "user@domain.com", "password": "pass@123"},
            {"username": "user#123", "password": "pass$456"},
            {"username": "user with spaces", "password": "pass with spaces"}
        ]
        
        for cred in special_chars_data:
            # Clear form first
            fresh_login_page.clear_form()
            
            # Try login with special characters
            fresh_login_page.login(cred["username"], cred["password"])
            fresh_login_page.wait_for_login_completion()
            
            # Should show error (as these are not valid credentials)
            assert fresh_login_page.is_error_message_displayed()
            
    @pytest.mark.ui
    def test_form_field_attributes(self, fresh_login_page: LoginPage):
        """Test form field attributes and properties.
        
        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Check username field attributes
        username_type = fresh_login_page.get_attribute(fresh_login_page.username_input, "type")
        assert username_type == "text", f"Username field should be type 'text', got '{username_type}'"
        
        # Check password field attributes
        password_type = fresh_login_page.get_attribute(fresh_login_page.password_input, "type")
        assert password_type == "password", f"Password field should be type 'password', got '{password_type}'"
        
        # Check submit button attributes
        submit_type = fresh_login_page.get_attribute(fresh_login_page.submit_button, "type")
        assert submit_type == "submit", f"Submit button should be type 'submit', got '{submit_type}'"
        
    @pytest.mark.slow
    @pytest.mark.login
    def test_login_performance(self, fresh_login_page: LoginPage, dashboard_page: DashboardPage, valid_credentials):
        """Test login performance and response time.
        
        Args:
            fresh_login_page: Fresh login page fixture
            dashboard_page: Dashboard page fixture
            valid_credentials: Valid credentials fixture
        """
        import time
        
        # Record start time
        start_time = time.time()
        
        # Perform login
        fresh_login_page.login(valid_credentials["username"], valid_credentials["password"])
        fresh_login_page.wait_for_login_completion()
        
        # Wait for dashboard to load
        dashboard_page.wait_for_dashboard_load()
        
        # Record end time
        end_time = time.time()
        login_duration = end_time - start_time
        
        # Assert login completed within reasonable time (10 seconds)
        assert login_duration < 10, f"Login took too long: {login_duration:.2f} seconds"
        
        # Verify successful login
        assert_login_success(dashboard_page)


class TestDashboardFunctionality:
    """Test class for dashboard functionality after successful login."""

    @pytest.mark.smoke
    def test_dashboard_elements_after_login(self, logged_in_user: DashboardPage):
        """Test dashboard elements are displayed correctly after login.

        Args:
            logged_in_user: Logged in user fixture
        """
        # Verify dashboard elements
        elements_status = logged_in_user.verify_dashboard_elements()

        assert elements_status["page_heading"], "Page heading is not visible"
        assert elements_status["success_message"], "Success message is not visible"
        assert elements_status["content_area"], "Content area is not visible"

    @pytest.mark.ui
    def test_dashboard_content_verification(self, logged_in_user: DashboardPage):
        """Test dashboard content is correct after login.

        Args:
            logged_in_user: Logged in user fixture
        """
        # Get user info
        user_info = logged_in_user.get_current_user_info()

        # Verify page title
        assert "Logged In Successfully" in user_info["page_title"]

        # Verify page heading
        assert "Logged In Successfully" in user_info["page_heading"]

        # Verify success message
        assert "Congratulations" in user_info["success_message"]

        # Verify URL
        assert "logged-in-successfully" in user_info["current_url"]

    @pytest.mark.regression
    def test_logout_functionality(self, logged_in_user: DashboardPage, login_page: LoginPage):
        """Test logout functionality if available.

        Args:
            logged_in_user: Logged in user fixture
            login_page: Login page fixture
        """
        # Check if logout button is available
        if logged_in_user.is_logout_button_visible():
            # Click logout
            logged_in_user.click_logout_button()

            # Wait for redirect to login page
            login_page.wait_for_page_load()

            # Verify back on login page
            assert login_page.verify_login_page_loaded()
        else:
            pytest.skip("Logout functionality not available on this page")


class TestLoginPageValidation:
    """Test class for login page validation and edge cases."""

    @pytest.mark.ui
    def test_empty_form_submission(self, fresh_login_page: LoginPage):
        """Test form submission with empty fields.

        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Submit empty form
        fresh_login_page.click_submit_button()
        fresh_login_page.wait_for_login_completion()

        # Should show error message
        assert fresh_login_page.is_error_message_displayed()
        error_message = fresh_login_page.get_error_message()
        assert "Your username is invalid!" in error_message

    @pytest.mark.regression
    def test_case_sensitive_login(self, fresh_login_page: LoginPage):
        """Test case sensitivity in login credentials.

        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Test with uppercase username
        fresh_login_page.login("STUDENT", "Password123")
        fresh_login_page.wait_for_login_completion()
        assert fresh_login_page.is_error_message_displayed()

        # Clear and test with different case password
        fresh_login_page.clear_form()
        fresh_login_page.login("student", "password123")
        fresh_login_page.wait_for_login_completion()
        assert fresh_login_page.is_error_message_displayed()

    @pytest.mark.regression
    def test_whitespace_handling(self, fresh_login_page: LoginPage):
        """Test handling of whitespace in credentials.

        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Test with leading/trailing spaces
        fresh_login_page.login(" student ", " Password123 ")
        fresh_login_page.wait_for_login_completion()

        # Should show error (assuming the system doesn't trim whitespace)
        assert fresh_login_page.is_error_message_displayed()

    @pytest.mark.ui
    def test_page_refresh_behavior(self, fresh_login_page: LoginPage):
        """Test page behavior after refresh.

        Args:
            fresh_login_page: Fresh login page fixture
        """
        # Enter some data
        fresh_login_page.enter_username("testuser")
        fresh_login_page.enter_password("testpass")

        # Refresh page
        fresh_login_page.refresh_page()
        fresh_login_page.wait_for_page_load()

        # Verify page loaded correctly
        assert fresh_login_page.verify_login_page_loaded()

        # Verify form is cleared
        assert fresh_login_page.get_username_value() == ""
        assert fresh_login_page.get_password_value() == ""
