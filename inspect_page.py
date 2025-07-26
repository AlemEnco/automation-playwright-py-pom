#!/usr/bin/env python3
"""Script to inspect the login page structure."""

from playwright.sync_api import sync_playwright


def inspect_login_page():
    """Inspect the login page to understand its structure."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to login page
            page.goto("https://practicetestautomation.com/practice-test-login/")
            page.wait_for_load_state("networkidle")
            
            print("🔍 Inspecting login page structure...")
            print("=" * 50)
            
            # Check page title
            title = page.title()
            print(f"Page title: {title}")
            
            # Check for form element
            forms = page.locator("form").count()
            print(f"Number of forms: {forms}")
            
            if forms > 0:
                form_html = page.locator("form").first.inner_html()
                print(f"Form HTML: {form_html[:200]}...")
            
            # Check for username input
            username_selectors = ["#username", "input[name='username']", "input[type='text']"]
            for selector in username_selectors:
                count = page.locator(selector).count()
                if count > 0:
                    print(f"Username selector '{selector}': {count} elements found")
                    element = page.locator(selector).first
                    print(f"  - Tag: {element.evaluate('el => el.tagName')}")
                    print(f"  - Type: {element.get_attribute('type')}")
                    print(f"  - Name: {element.get_attribute('name')}")
                    print(f"  - ID: {element.get_attribute('id')}")
            
            # Check for password input
            password_selectors = ["#password", "input[name='password']", "input[type='password']"]
            for selector in password_selectors:
                count = page.locator(selector).count()
                if count > 0:
                    print(f"Password selector '{selector}': {count} elements found")
                    element = page.locator(selector).first
                    print(f"  - Tag: {element.evaluate('el => el.tagName')}")
                    print(f"  - Type: {element.get_attribute('type')}")
                    print(f"  - Name: {element.get_attribute('name')}")
                    print(f"  - ID: {element.get_attribute('id')}")
            
            # Check for submit button
            submit_selectors = ["#submit", "input[type='submit']", "button[type='submit']", "button"]
            for selector in submit_selectors:
                count = page.locator(selector).count()
                if count > 0:
                    print(f"Submit selector '{selector}': {count} elements found")
                    element = page.locator(selector).first
                    print(f"  - Tag: {element.evaluate('el => el.tagName')}")
                    print(f"  - Type: {element.get_attribute('type')}")
                    print(f"  - ID: {element.get_attribute('id')}")
                    print(f"  - Text: {element.text_content()}")
            
            # Check for headings
            headings = page.locator("h1, h2, h3").all()
            print(f"\nHeadings found: {len(headings)}")
            for i, heading in enumerate(headings):
                print(f"  {i+1}. {heading.tag_name()}: {heading.text_content()}")
            
            # Get page HTML structure (first 1000 chars)
            body_html = page.locator("body").inner_html()
            print(f"\nPage body structure (first 1000 chars):")
            print(body_html[:1000])
            
        except Exception as e:
            print(f"Error inspecting page: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    inspect_login_page()
