"""Dashboard/Home Page Object Model class."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page Object Model for the dashboard/home page after successful login."""
    
    def __init__(self, page: Page):
        """Initialize the dashboard page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        
        # Page locators
        self.page_heading = "h1"
        self.success_message = ".post-title"
        self.logout_button = "a[href*='logout']"
        self.content_area = ".post-content"
        self.navigation_menu = "nav"
        
        # Expected elements and text
        self.expected_heading = "Logged In Successfully"
        self.expected_success_message = "Logged In Successfully"  # Updated to match actual page content
        self.expected_url_pattern = "logged-in-successfully"
        
    def verify_successful_login(self) -> bool:
        """Verify that login was successful and dashboard page loaded.
        
        Returns:
            True if login was successful and dashboard loaded, False otherwise
        """
        try:
            # Check if URL contains the expected pattern
            current_url = self.get_url()
            if self.expected_url_pattern not in current_url:
                self.logger.error(f"Expected URL to contain '{self.expected_url_pattern}', but got '{current_url}'")
                return False
                
            # Check if success heading is visible
            if not self.is_element_visible(self.page_heading):
                self.logger.error("Page heading is not visible")
                return False
                
            # Verify the heading text
            heading_text = self.get_page_heading()
            if self.expected_heading not in heading_text:
                self.logger.error(f"Expected heading to contain '{self.expected_heading}', but got '{heading_text}'")
                return False
                
            # Check if success message is visible
            if not self.is_element_visible(self.success_message):
                self.logger.error("Success message is not visible")
                return False
                
            self.logger.info("Dashboard page loaded successfully after login")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying successful login: {str(e)}")
            return False
            
    def get_page_heading(self) -> str:
        """Get the main page heading text.
        
        Returns:
            Page heading text
        """
        return self.get_text(self.page_heading)
        
    def get_success_message(self) -> str:
        """Get the success message text.
        
        Returns:
            Success message text
        """
        return self.get_text(self.success_message)
        
    def is_logout_button_visible(self) -> bool:
        """Check if logout button is visible.
        
        Returns:
            True if logout button is visible, False otherwise
        """
        return self.is_element_visible(self.logout_button, timeout=5000)
        
    def click_logout_button(self) -> None:
        """Click the logout button if available."""
        if self.is_logout_button_visible():
            self.logger.info("Clicking logout button")
            self.click_element(self.logout_button)
        else:
            self.logger.warning("Logout button is not visible")
            
    def get_page_content(self) -> str:
        """Get the main content area text.
        
        Returns:
            Content area text
        """
        if self.is_element_visible(self.content_area):
            return self.get_text(self.content_area)
        return ""
        
    def verify_dashboard_elements(self) -> dict:
        """Verify all expected dashboard elements are present.
        
        Returns:
            Dictionary with verification results for each element
        """
        verification_results = {
            "page_heading": self.is_element_visible(self.page_heading),
            "success_message": self.is_element_visible(self.success_message),
            "content_area": self.is_element_visible(self.content_area),
            "logout_button": self.is_logout_button_visible()
        }
        
        self.logger.info(f"Dashboard elements verification: {verification_results}")
        return verification_results
        
    def wait_for_dashboard_load(self, timeout: int = 10000) -> bool:
        """Wait for dashboard page to load completely.
        
        Args:
            timeout: Timeout in milliseconds
            
        Returns:
            True if dashboard loaded successfully, False if timeout
        """
        try:
            # Wait for the main heading to be visible
            self.wait_for_element(self.page_heading, timeout)
            
            # Wait for page to be fully loaded
            self.wait_for_page_load()
            
            self.logger.info("Dashboard page loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Timeout waiting for dashboard to load: {str(e)}")
            return False
            
    def get_current_user_info(self) -> dict:
        """Extract any user information displayed on the dashboard.
        
        Returns:
            Dictionary with user information if available
        """
        user_info = {
            "page_title": self.get_title(),
            "page_heading": self.get_page_heading(),
            "success_message": self.get_success_message(),
            "current_url": self.get_url()
        }
        
        self.logger.info(f"Current user info: {user_info}")
        return user_info
        
    def verify_login_success_indicators(self) -> list:
        """Verify multiple indicators that login was successful.
        
        Returns:
            List of verification results with descriptions
        """
        indicators = []
        
        # Check URL change
        current_url = self.get_url()
        url_check = self.expected_url_pattern in current_url
        indicators.append({
            "indicator": "URL contains success pattern",
            "expected": self.expected_url_pattern,
            "actual": current_url,
            "passed": url_check
        })
        
        # Check page heading
        heading_text = self.get_page_heading()
        heading_check = self.expected_heading in heading_text
        indicators.append({
            "indicator": "Page heading indicates success",
            "expected": self.expected_heading,
            "actual": heading_text,
            "passed": heading_check
        })
        
        # Check success message
        success_text = self.get_success_message()
        success_check = self.expected_success_message in success_text
        indicators.append({
            "indicator": "Success message is displayed",
            "expected": self.expected_success_message,
            "actual": success_text,
            "passed": success_check
        })
        
        self.logger.info(f"Login success indicators: {indicators}")
        return indicators
