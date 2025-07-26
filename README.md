# Playwright Python Test Automation with Page Object Model

This project demonstrates test automation using Playwright with Python and pytest, implementing the Page Object Model (POM) design pattern.

## Project Structure

```
automation-playwright-py-pom/
├── pages/                  # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py       # Base page with common functionality
│   ├── login_page.py      # Login page object
│   └── dashboard_page.py  # Dashboard/home page object
├── tests/                 # Test cases
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and configuration
│   └── test_login.py      # Login functionality tests
├── utils/                 # Utility functions and helpers
│   ├── __init__.py
│   └── test_data.py       # Test data management
├── reports/               # Test reports (generated)
├── logs/                  # Log files (generated)
├── requirements.txt       # Python dependencies
├── pytest.ini           # Pytest configuration
├── playwright.config.py  # Playwright configuration
└── .env                  # Environment variables
```

## Setup Instructions

### Quick Setup (Recommended)

1. **Run the automated setup script:**
   ```bash
   python3 setup.py
   ```
   This will:
   - Check Python version compatibility
   - Install all dependencies
   - Install Playwright browsers
   - Create necessary directories
   - Verify the installation

### Python 3.13 Compatibility

If you encounter build errors with Python 3.13, use the compatibility installer:

```bash
python3 install_dependencies.py
```

Or install with binary-only packages:
```bash
pip3 install playwright --only-binary=all
pip3 install pytest-playwright --only-binary=all
pip3 install pytest python-dotenv
python3 -m playwright install
```

### Manual Setup

1. **Check Python version (3.8+ required):**
   ```bash
   python3 --version
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   python3 -m playwright install
   ```

4. **Create necessary directories:**
   ```bash
   mkdir -p reports/screenshots reports/videos logs
   ```

5. **Verify installation:**
   ```bash
   python3 validate_project.py
   ```

## Running Tests

### Using the Test Runner (Recommended)

```bash
# Run all tests
python3 run_tests.py

# Run smoke tests only
python3 run_tests.py --smoke

# Run login tests only
python3 run_tests.py --login

# Run tests in headless mode
python3 run_tests.py --headless

# Run tests in parallel
python3 run_tests.py --parallel

# Generate HTML report
python3 run_tests.py --html-report

# Run specific test file
python3 run_tests.py --test-file tests/test_login.py

# Run specific test function
python3 run_tests.py --test-function test_valid_login_success
```

### Using Pytest Directly

```bash
# Run all tests
pytest

# Run with specific markers
pytest -m smoke
pytest -m login
pytest -m ui
pytest -m regression

# Run in headless mode
pytest --headed=false

# Run with parallel execution
pytest -n auto

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_login.py

# Run specific test function
pytest -k "test_valid_login_success"
```

## Test Target

The tests are designed to run against: https://practicetestautomation.com/practice-test-login/

## Features

- **Page Object Model (POM)**: Clean separation between page logic and test logic
- **Pytest Integration**: Full pytest support with fixtures and markers
- **Multiple Browser Support**: Chromium, Firefox, and WebKit
- **Parallel Execution**: Run tests in parallel using pytest-xdist
- **HTML Reports**: Generate detailed HTML test reports
- **Screenshots and Videos**: Capture on test failures
- **Environment Configuration**: Flexible configuration through environment variables

## Test Coverage

### Login Functionality Tests
- ✅ Valid login with correct credentials
- ✅ Invalid login scenarios (wrong username/password)
- ✅ Empty form submission
- ✅ Case sensitivity testing
- ✅ Whitespace handling
- ✅ Special characters in credentials
- ✅ Multiple login attempts

### UI Validation Tests
- ✅ Page element visibility
- ✅ Form field interactions
- ✅ Button states and attributes
- ✅ Error message display
- ✅ Page title and heading verification
- ✅ Page refresh behavior

### Dashboard Tests
- ✅ Successful login verification
- ✅ Dashboard element validation
- ✅ Content verification
- ✅ Logout functionality (if available)

### Performance Tests
- ✅ Login response time validation

## Project Features

- **Page Object Model (POM)**: Clean separation of concerns
- **Pytest Integration**: Full pytest support with fixtures and markers
- **Multiple Browser Support**: Chromium, Firefox, and WebKit
- **Parallel Execution**: Run tests in parallel using pytest-xdist
- **HTML Reports**: Generate detailed HTML test reports
- **Screenshots and Videos**: Capture on test failures
- **Environment Configuration**: Flexible configuration through environment variables
- **Comprehensive Logging**: Detailed logging for debugging
- **Test Data Management**: Centralized test data management
- **Custom Assertions**: Domain-specific assertion helpers

## Configuration

### Environment Variables (.env)
```
BASE_URL=https://practicetestautomation.com
LOGIN_URL=https://practicetestautomation.com/practice-test-login/
BROWSER=chromium
HEADLESS=false
TIMEOUT=30000
```

### Pytest Configuration (pytest.ini)
- Test discovery patterns
- Custom markers
- Default command-line options
- HTML reporting configuration

### Playwright Configuration (playwright.config.py)
- Browser settings
- Viewport configuration
- Video and screenshot settings
- Timeout configurations
- Test credentials

## Troubleshooting

### Quick Fixes

1. **Python 3.13 build errors (greenlet)**
   ```bash
   python3 install_dependencies.py
   ```

2. **Playwright not found**
   ```bash
   python3 -m pip install playwright
   python3 -m playwright install
   ```

3. **Tests failing due to timeouts**
   ```bash
   pytest --slow-mo=1000
   ```

4. **Browser not launching**
   ```bash
   python3 -m playwright install
   # Or run in headless mode
   pytest --headed=false
   ```

5. **Import errors**
   ```bash
   python3 validate_project.py
   ```

### Comprehensive Troubleshooting

For detailed troubleshooting including Python 3.13 compatibility issues, platform-specific problems, and alternative installation methods, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

### Debug Mode

Run tests with debug information:
```bash
# Enable debug logging
pytest --log-cli-level=DEBUG

# Run single test with maximum verbosity
pytest -v -s tests/test_login.py::TestLoginFunctionality::test_valid_login_success
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new functionality
3. Update documentation
4. Ensure all tests pass before submitting

## License

This project is for educational purposes and demonstrates best practices in test automation.
