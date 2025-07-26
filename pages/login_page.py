"""Login Page Object Model class."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
try:
    from playwright.config import LOGIN_URL
except ImportError:
    # Fallback URL if config import fails
    LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"
import logging


class LoginPage(BasePage):
    """Page Object Model for the login page."""
    
    def __init__(self, page: Page):
        """Initialize the login page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = LOGIN_URL
        
        # Page locators
        self.username_input = "#username"
        self.password_input = "#password"
        self.submit_button = "#submit"
        self.error_message = "#error"
        self.page_title = "h1, h2"
        self.login_form = ".wp-block-group"  # Updated to use a more generic container
        
        # Expected elements and text
        self.expected_title = "Test Login"
        self.expected_page_heading = "Practice Test Login"
        
    def navigate_to_login_page(self) -> None:
        """Navigate to the login page."""
        self.logger.info(f"Navigating to login page: {self.url}")
        self.navigate_to(self.url)
        self.wait_for_page_load()
        
    def verify_login_page_loaded(self) -> bool:
        """Verify that the login page has loaded correctly.
        
        Returns:
            True if login page is loaded correctly, False otherwise
        """
        try:
            # Check if the page title is correct
            page_title = self.get_title()
            if self.expected_title not in page_title:
                self.logger.error(f"Expected title to contain '{self.expected_title}', but got '{page_title}'")
                return False
                
            # Check if main elements are visible
            if not self.is_element_visible(self.username_input):
                self.logger.error("Username input field is not visible")
                return False
                
            if not self.is_element_visible(self.password_input):
                self.logger.error("Password input field is not visible")
                return False
                
            if not self.is_element_visible(self.submit_button):
                self.logger.error("Submit button is not visible")
                return False
                
            self.logger.info("Login page loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying login page: {str(e)}")
            return False
            
    def enter_username(self, username: str) -> None:
        """Enter username in the username field.
        
        Args:
            username: Username to enter
        """
        self.logger.info(f"Entering username: {username}")
        self.fill_text(self.username_input, username)
        
    def enter_password(self, password: str) -> None:
        """Enter password in the password field.
        
        Args:
            password: Password to enter
        """
        self.logger.info("Entering password")
        self.fill_text(self.password_input, password)
        
    def click_submit_button(self) -> None:
        """Click the submit/login button."""
        self.logger.info("Clicking submit button")
        self.click_element(self.submit_button)
        
    def login(self, username: str, password: str) -> None:
        """Perform complete login action.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        self.logger.info(f"Performing login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit_button()
        
    def get_error_message(self) -> str:
        """Get the error message text if displayed.
        
        Returns:
            Error message text or empty string if no error
        """
        try:
            if self.is_element_visible(self.error_message, timeout=5000):
                error_text = self.get_text(self.error_message)
                self.logger.info(f"Error message found: {error_text}")
                return error_text
            else:
                self.logger.info("No error message displayed")
                return ""
        except Exception as e:
            self.logger.error(f"Error getting error message: {str(e)}")
            return ""
            
    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed.
        
        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.error_message, timeout=5000)
        
    def clear_username_field(self) -> None:
        """Clear the username input field."""
        self.logger.info("Clearing username field")
        username_element = self.wait_for_element(self.username_input)
        username_element.clear()
        
    def clear_password_field(self) -> None:
        """Clear the password input field."""
        self.logger.info("Clearing password field")
        password_element = self.wait_for_element(self.password_input)
        password_element.clear()
        
    def clear_form(self) -> None:
        """Clear both username and password fields."""
        self.logger.info("Clearing login form")
        self.clear_username_field()
        self.clear_password_field()
        
    def get_username_value(self) -> str:
        """Get the current value in the username field.

        Returns:
            Current username field value
        """
        element = self.wait_for_element(self.username_input)
        return element.input_value()

    def get_password_value(self) -> str:
        """Get the current value in the password field.

        Returns:
            Current password field value
        """
        element = self.wait_for_element(self.password_input)
        return element.input_value()
        
    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is enabled.
        
        Returns:
            True if submit button is enabled, False otherwise
        """
        return self.is_element_enabled(self.submit_button)
        
    def get_page_heading(self) -> str:
        """Get the main page heading text.
        
        Returns:
            Page heading text
        """
        return self.get_text(self.page_title)
        
    def verify_page_elements(self) -> dict:
        """Verify all expected page elements are present and return status.
        
        Returns:
            Dictionary with verification results for each element
        """
        verification_results = {
            "username_input": self.is_element_visible(self.username_input),
            "password_input": self.is_element_visible(self.password_input),
            "submit_button": self.is_element_visible(self.submit_button),
            "login_form": self.is_element_visible(self.login_form),
            "page_title": self.is_element_visible(self.page_title)
        }
        
        self.logger.info(f"Page elements verification: {verification_results}")
        return verification_results
        
    def wait_for_login_completion(self, timeout: int = 10000) -> bool:
        """Wait for login process to complete (either success or error).

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if login completed (success or error), False if timeout
        """
        try:
            current_url = self.url
            # Wait for either URL change (success) or error message (failure)
            self.page.wait_for_function(
                f"""() => {{
                    return window.location.href !== '{current_url}' ||
                           document.querySelector('#error') !== null;
                }}""",
                timeout=timeout
            )
            return True

        except Exception as e:
            self.logger.error(f"Timeout waiting for login completion: {str(e)}")
            return False
