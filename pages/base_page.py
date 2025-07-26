from playwright.sync_api import Page, Locator, expect
from typing import Optional, Union
import logging
try:
    from playwright.config import ELEMENT_TIMEOUT, DEFAULT_TIMEOUT
except ImportError:
    # Fallback values if config import fails
    ELEMENT_TIMEOUT = 10000
    DEFAULT_TIMEOUT = 30000


class BasePage:
    """Base page class containing common functionality for all page objects."""
    
    def __init__(self, page: Page):
        """Initialize the base page with a Playwright page instance.
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL.
        
        Args:
            url: The URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=DEFAULT_TIMEOUT)
        
    def get_title(self) -> str:
        """Get the page title.
        
        Returns:
            The page title
        """
        return self.page.title()
        
    def get_url(self) -> str:
        """Get the current page URL.
        
        Returns:
            The current URL
        """
        return self.page.url
        
    def wait_for_element(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> Locator:
        """Wait for an element to be visible.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
            
        Returns:
            Locator object
        """
        if isinstance(locator, str):
            element = self.page.locator(locator)
        else:
            element = locator
            
        element.wait_for(state="visible", timeout=timeout)
        return element
        
    def wait_for_element_hidden(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> None:
        """Wait for an element to be hidden.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
        """
        if isinstance(locator, str):
            element = self.page.locator(locator)
        else:
            element = locator
            
        element.wait_for(state="hidden", timeout=timeout)
        
    def click_element(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> None:
        """Click on an element.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
        """
        element = self.wait_for_element(locator, timeout)
        self.logger.info(f"Clicking element: {locator}")
        element.click()
        
    def fill_text(self, locator: Union[str, Locator], text: str, timeout: int = ELEMENT_TIMEOUT) -> None:
        """Fill text into an input field.
        
        Args:
            locator: Element locator (string or Locator object)
            text: Text to fill
            timeout: Timeout in milliseconds
        """
        element = self.wait_for_element(locator, timeout)
        self.logger.info(f"Filling text '{text}' into element: {locator}")
        element.clear()
        element.fill(text)
        
    def get_text(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> str:
        """Get text content from an element.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
            
        Returns:
            Text content of the element
        """
        element = self.wait_for_element(locator, timeout)
        return element.text_content() or ""
        
    def is_element_visible(self, locator: Union[str, Locator], timeout: int = 5000) -> bool:
        """Check if an element is visible.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            if isinstance(locator, str):
                element = self.page.locator(locator)
            else:
                element = locator
            element.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
            
    def is_element_enabled(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> bool:
        """Check if an element is enabled.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
            
        Returns:
            True if element is enabled, False otherwise
        """
        element = self.wait_for_element(locator, timeout)
        return element.is_enabled()
        
    def get_attribute(self, locator: Union[str, Locator], attribute: str, timeout: int = ELEMENT_TIMEOUT) -> Optional[str]:
        """Get an attribute value from an element.
        
        Args:
            locator: Element locator (string or Locator object)
            attribute: Attribute name
            timeout: Timeout in milliseconds
            
        Returns:
            Attribute value or None if not found
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute)
        
    def scroll_to_element(self, locator: Union[str, Locator], timeout: int = ELEMENT_TIMEOUT) -> None:
        """Scroll to an element.
        
        Args:
            locator: Element locator (string or Locator object)
            timeout: Timeout in milliseconds
        """
        element = self.wait_for_element(locator, timeout)
        element.scroll_into_view_if_needed()
        
    def take_screenshot(self, filename: str) -> None:
        """Take a screenshot of the current page.
        
        Args:
            filename: Screenshot filename
        """
        self.logger.info(f"Taking screenshot: {filename}")
        self.page.screenshot(path=f"reports/{filename}")
        
    def wait_for_page_load(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Wait for page to load completely.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        
    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.info("Refreshing page")
        self.page.reload()
        
    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.logger.info("Navigating back")
        self.page.go_back()
        
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.logger.info("Navigating forward")
        self.page.go_forward()
