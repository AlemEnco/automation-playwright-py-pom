"""Pytest configuration and fixtures for test automation."""

import pytest
import logging
import os
from datetime import datetime
from playwright.sync_api import BrowserContext, Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
try:
    from playwright.config import PLAYWRIGHT_CONFIG, VALID_CREDENTIALS, INVALID_CREDENTIALS
except ImportError:
    # Fallback configuration if config import fails
    PLAYWRIGHT_CONFIG = {
        "browser_name": "chromium",
        "headless": False,
        "slow_mo": 500,
        "viewport": {"width": 1280, "height": 720}
    }
    VALID_CREDENTIALS = {"username": "student", "password": "Password123"}
    INVALID_CREDENTIALS = [
        {"username": "incorrectUser", "password": "Password123", "expected_error": "Your username is invalid!"},
        {"username": "student", "password": "incorrectPassword", "expected_error": "Your password is invalid!"}
    ]
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
def setup_logging():
    """Set up logging configuration."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Set up logging at module level
logger = setup_logging()


@pytest.fixture(scope="session")
def playwright_config():
    """Provide Playwright configuration."""
    return PLAYWRIGHT_CONFIG


@pytest.fixture(scope="session")
def browser_type_launch_args(playwright_config):
    """Configure browser launch arguments."""
    return {
        "headless": playwright_config.get("headless", False),
        "slow_mo": playwright_config.get("slow_mo", 500),
        "args": ["--start-maximized"] if not playwright_config.get("headless", False) else []
    }


@pytest.fixture(scope="session")
def browser_context_args(playwright_config):
    """Configure browser context arguments."""
    return {
        "viewport": playwright_config.get("viewport", {"width": 1280, "height": 720}),
        "record_video_dir": "reports/videos" if playwright_config.get("video") else None,
        "record_video_size": {"width": 1280, "height": 720}
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    
    # Set default timeouts
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    # Add screenshot on failure
    yield page
    
    # Cleanup
    page.close()


@pytest.fixture(scope="function")
def login_page(page: Page):
    """Create a LoginPage instance."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(page: Page):
    """Create a DashboardPage instance."""
    return DashboardPage(page)


@pytest.fixture(scope="function")
def valid_credentials():
    """Provide valid login credentials."""
    return VALID_CREDENTIALS.copy()


@pytest.fixture(scope="function")
def invalid_credentials():
    """Provide invalid login credentials test data."""
    return INVALID_CREDENTIALS.copy()


@pytest.fixture(scope="function")
def test_data():
    """Provide comprehensive test data."""
    return {
        "valid_credentials": VALID_CREDENTIALS.copy(),
        "invalid_credentials": INVALID_CREDENTIALS.copy(),
        "empty_credentials": {"username": "", "password": ""},
        "special_characters": {
            "username": "test@#$%",
            "password": "pass@#$%123"
        }
    }


@pytest.fixture(autouse=True)
def setup_test_environment(request, page: Page):
    """Set up test environment before each test."""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    
    yield
    
    # Take screenshot on test failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"failure_{test_name}_{timestamp}.png"
        screenshot_path = os.path.join("reports/screenshots", screenshot_name)
        page.screenshot(path=screenshot_path)
        logger.error(f"Test failed. Screenshot saved: {screenshot_path}")
    
    logger.info(f"Completed test: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def logged_in_user(login_page: LoginPage, dashboard_page: DashboardPage, valid_credentials):
    """Fixture that provides a logged-in user session."""
    # Navigate to login page
    login_page.navigate_to_login_page()
    
    # Verify login page loaded
    assert login_page.verify_login_page_loaded(), "Login page did not load correctly"
    
    # Perform login
    login_page.login(valid_credentials["username"], valid_credentials["password"])
    
    # Wait for login completion
    assert login_page.wait_for_login_completion(), "Login did not complete in expected time"
    
    # Verify successful login
    assert dashboard_page.verify_successful_login(), "Login was not successful"
    
    yield dashboard_page
    
    # Cleanup: logout if possible
    try:
        if dashboard_page.is_logout_button_visible():
            dashboard_page.click_logout_button()
    except Exception as e:
        logger.warning(f"Could not logout: {str(e)}")


@pytest.fixture(scope="function")
def fresh_login_page(login_page: LoginPage):
    """Fixture that provides a fresh login page for each test."""
    login_page.navigate_to_login_page()
    assert login_page.verify_login_page_loaded(), "Login page did not load correctly"
    return login_page


# Pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login functionality test")
    config.addinivalue_line("markers", "ui: mark test as UI validation test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


# Custom assertions
def assert_login_success(dashboard_page: DashboardPage):
    """Custom assertion for successful login."""
    indicators = dashboard_page.verify_login_success_indicators()
    failed_indicators = [ind for ind in indicators if not ind["passed"]]
    
    if failed_indicators:
        failure_messages = [f"{ind['indicator']}: expected '{ind['expected']}', got '{ind['actual']}'" 
                          for ind in failed_indicators]
        pytest.fail(f"Login success verification failed:\n" + "\n".join(failure_messages))


def assert_login_failure(login_page: LoginPage, expected_error: str):
    """Custom assertion for login failure with specific error message."""
    assert login_page.is_error_message_displayed(), "Expected error message to be displayed"
    actual_error = login_page.get_error_message()
    assert expected_error in actual_error, f"Expected error '{expected_error}', but got '{actual_error}'"
