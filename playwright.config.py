"""Playwright configuration file for test automation."""

from playwright.sync_api import Playwright
import os

def pytest_configure():
    """Configure pytest with Playwright settings."""
    pass

# Playwright configuration
PLAYWRIGHT_CONFIG = {
    "browser_name": "chromium",
    "headless": False,
    "slow_mo": 500,
    "viewport": {"width": 1280, "height": 720},
    "video": "retain-on-failure",
    "screenshot": "only-on-failure",
    "trace": "retain-on-failure"
}

# Test configuration
BASE_URL = "https://practicetestautomation.com"
LOGIN_URL = f"{BASE_URL}/practice-test-login/"

# Timeouts (in milliseconds)
DEFAULT_TIMEOUT = 30000
ELEMENT_TIMEOUT = 10000
NAVIGATION_TIMEOUT = 30000

# Test data
VALID_CREDENTIALS = {
    "username": "student",
    "password": "Password123"
}

INVALID_CREDENTIALS = [
    {"username": "incorrectUser", "password": "Password123", "expected_error": "Your username is invalid!"},
    {"username": "student", "password": "incorrectPassword", "expected_error": "Your password is invalid!"},
    {"username": "", "password": "Password123", "expected_error": "Your username is invalid!"},
    {"username": "student", "password": "", "expected_error": "Your password is invalid!"}
]
