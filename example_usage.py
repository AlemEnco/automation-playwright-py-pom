#!/usr/bin/env python3
"""Example usage of the Playwright Python test automation framework."""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.test_data import TestDataManager, get_default_valid_credentials


def example_manual_test():
    """Example of how to use the page objects manually (without pytest)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright not installed. Please run: python3 setup.py")
        return False
    
    print("🎭 Example: Manual test using Playwright page objects")
    print("-" * 50)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        try:
            # Create page objects
            login_page = LoginPage(page)
            dashboard_page = DashboardPage(page)
            
            # Navigate to login page
            print("📍 Navigating to login page...")
            login_page.navigate_to_login_page()
            
            # Verify login page loaded
            print("🔍 Verifying login page loaded...")
            if not login_page.verify_login_page_loaded():
                print("❌ Login page did not load correctly")
                return False
            print("✅ Login page loaded successfully")
            
            # Get valid credentials
            credentials = get_default_valid_credentials()
            
            # Perform login
            print(f"🔐 Logging in with username: {credentials.username}")
            login_page.login(credentials.username, credentials.password)
            
            # Wait for login completion
            print("⏳ Waiting for login completion...")
            if not login_page.wait_for_login_completion():
                print("❌ Login did not complete in expected time")
                return False
            
            # Verify successful login
            print("🔍 Verifying successful login...")
            if not dashboard_page.verify_successful_login():
                print("❌ Login was not successful")
                return False
            
            print("✅ Login successful!")
            
            # Get dashboard information
            user_info = dashboard_page.get_current_user_info()
            print(f"📊 Dashboard info:")
            print(f"   - Page title: {user_info['page_title']}")
            print(f"   - Page heading: {user_info['page_heading']}")
            print(f"   - Success message: {user_info['success_message']}")
            print(f"   - Current URL: {user_info['current_url']}")
            
            # Take a screenshot
            print("📸 Taking screenshot...")
            dashboard_page.take_screenshot("example_success.png")
            
            print("🎉 Example test completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during test execution: {e}")
            return False
            
        finally:
            # Cleanup
            browser.close()


def example_test_data_usage():
    """Example of how to use the test data manager."""
    print("\n📊 Example: Using Test Data Manager")
    print("-" * 40)
    
    # Create test data manager
    data_manager = TestDataManager()
    
    # Get valid credentials
    valid_creds = data_manager.get_valid_credentials()
    print(f"Valid credentials found: {len(valid_creds)}")
    for cred in valid_creds:
        print(f"   - Username: {cred.username}, Expected: {cred.expected_result}")
    
    # Get invalid credentials
    invalid_creds = data_manager.get_invalid_credentials()
    print(f"\nInvalid credentials found: {len(invalid_creds)}")
    for cred in invalid_creds:
        print(f"   - Username: {cred.username}, Error: {cred.expected_error}")
    
    # Get boundary test data
    boundary_data = data_manager.get_boundary_test_data()
    print(f"\nBoundary test data: {boundary_data}")
    
    # Get security test data
    security_data = data_manager.get_security_test_data()
    print(f"\nSecurity test data: {security_data}")


def example_page_object_features():
    """Example of page object features (without browser)."""
    print("\n🏗️  Example: Page Object Features")
    print("-" * 40)
    
    print("LoginPage features:")
    print("   - navigate_to_login_page()")
    print("   - verify_login_page_loaded()")
    print("   - enter_username(username)")
    print("   - enter_password(password)")
    print("   - login(username, password)")
    print("   - get_error_message()")
    print("   - is_error_message_displayed()")
    print("   - clear_form()")
    print("   - verify_page_elements()")
    
    print("\nDashboardPage features:")
    print("   - verify_successful_login()")
    print("   - get_page_heading()")
    print("   - get_success_message()")
    print("   - get_current_user_info()")
    print("   - verify_dashboard_elements()")
    print("   - wait_for_dashboard_load()")
    
    print("\nBasePage features (inherited by all pages):")
    print("   - navigate_to(url)")
    print("   - get_title()")
    print("   - get_url()")
    print("   - wait_for_element(locator)")
    print("   - click_element(locator)")
    print("   - fill_text(locator, text)")
    print("   - get_text(locator)")
    print("   - is_element_visible(locator)")
    print("   - take_screenshot(filename)")
    print("   - wait_for_page_load()")


def main():
    """Main example function."""
    print("🎯 Playwright Python Test Automation Framework Examples")
    print("=" * 60)
    
    # Show page object features
    example_page_object_features()
    
    # Show test data usage
    example_test_data_usage()
    
    # Ask user if they want to run the manual test
    print("\n" + "=" * 60)
    response = input("Do you want to run the manual browser test? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        success = example_manual_test()
        if success:
            print("\n🎉 All examples completed successfully!")
            return 0
        else:
            print("\n❌ Manual test failed")
            return 1
    else:
        print("\n✅ Examples completed (manual test skipped)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
