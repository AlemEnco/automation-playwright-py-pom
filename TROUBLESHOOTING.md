# Troubleshooting Guide

This guide helps resolve common installation and runtime issues with the Playwright Python test automation project.

## Python 3.13 Compatibility Issues

### Problem: greenlet build errors
```
error: command '/usr/bin/clang++' failed with exit code 1
Building wheel for greenlet (pyproject.toml) ... error
```

### Solutions (try in order):

#### Option 1: Use the compatibility installer
```bash
python3 install_dependencies.py
```

#### Option 2: Install with binary-only packages
```bash
pip3 install --upgrade pip
pip3 install playwright --only-binary=all
pip3 install pytest-playwright --only-binary=all
pip3 install pytest python-dotenv
playwright install
```

#### Option 3: Use conda (recommended for Python 3.13)
```bash
# Install conda/miniconda first, then:
conda create -n playwright-env python=3.12
conda activate playwright-env
conda install -c conda-forge playwright pytest
pip install pytest-playwright python-dotenv
playwright install
```

#### Option 4: Use Python 3.11 or 3.12
```bash
# Install Python 3.12 using pyenv or homebrew
brew install python@3.12
python3.12 -m pip install -r requirements.txt
python3.12 -m playwright install
```

## Common Installation Issues

### Issue: "playwright: command not found"
**Solution:**
```bash
python3 -m playwright install
# or
pip3 install playwright
python3 -m playwright install
```

### Issue: "No module named 'playwright'"
**Solution:**
```bash
pip3 install playwright
# Verify installation:
python3 -c "import playwright; print('Playwright installed successfully')"
```

### Issue: Browser download fails
**Solution:**
```bash
# Clear playwright cache and reinstall
rm -rf ~/.cache/ms-playwright
python3 -m playwright install
```

### Issue: Permission denied errors
**Solution:**
```bash
# Use user installation
pip3 install --user -r requirements.txt
python3 -m playwright install
```

## Runtime Issues

### Issue: Tests fail with timeout errors
**Solutions:**
1. Increase timeouts in `playwright.config.py`
2. Run with slower execution:
   ```bash
   pytest --slow-mo=1000
   ```
3. Check internet connection
4. Run in headless mode:
   ```bash
   pytest --headed=false
   ```

### Issue: Browser won't launch
**Solutions:**
1. Install browsers:
   ```bash
   python3 -m playwright install
   ```
2. Run in headless mode:
   ```bash
   pytest --headed=false
   ```
3. Check system requirements (Linux users may need additional packages)

### Issue: Import errors in tests
**Solutions:**
1. Ensure you're in the project root directory
2. Check Python path:
   ```bash
   python3 validate_project.py
   ```
3. Reinstall dependencies:
   ```bash
   python3 install_dependencies.py
   ```

## Platform-Specific Issues

### macOS Issues
- **Xcode command line tools required:**
  ```bash
  xcode-select --install
  ```
- **Homebrew Python conflicts:**
  ```bash
  # Use system Python or pyenv
  pyenv install 3.12.0
  pyenv local 3.12.0
  ```

### Linux Issues
- **Missing system dependencies:**
  ```bash
  # Ubuntu/Debian:
  sudo apt-get update
  sudo apt-get install -y python3-dev build-essential
  
  # CentOS/RHEL:
  sudo yum install python3-devel gcc gcc-c++
  ```

### Windows Issues
- **Visual Studio Build Tools required:**
  - Install Visual Studio Build Tools 2019 or later
  - Or use pre-built wheels: `pip install --only-binary=all`

## Testing the Installation

### Quick validation
```bash
python3 validate_project.py
```

### Manual verification
```bash
# Test imports
python3 -c "
import playwright
import pytest
from pages.login_page import LoginPage
print('All imports successful!')
"

# Test browser installation
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    print('Browser launch successful!')
    browser.close()
"
```

## Alternative Installation Methods

### Method 1: Docker (most reliable)
```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest"]
EOF

# Build and run
docker build -t playwright-tests .
docker run -v $(pwd)/reports:/app/reports playwright-tests
```

### Method 2: Virtual environment with specific Python version
```bash
# Using pyenv
pyenv install 3.11.7
pyenv virtualenv 3.11.7 playwright-env
pyenv activate playwright-env
pip install -r requirements.txt
playwright install
```

### Method 3: Poetry (dependency management)
```bash
# Install poetry first
curl -sSL https://install.python-poetry.org | python3 -

# Create pyproject.toml
poetry init
poetry add playwright pytest pytest-playwright python-dotenv
poetry install
poetry run playwright install
```

## Getting Help

If none of these solutions work:

1. **Check the project validation:**
   ```bash
   python3 validate_project.py
   ```

2. **Run with verbose output:**
   ```bash
   pip3 install -v playwright
   ```

3. **Check system compatibility:**
   ```bash
   python3 -c "
   import sys, platform
   print(f'Python: {sys.version}')
   print(f'Platform: {platform.platform()}')
   print(f'Architecture: {platform.architecture()}')
   "
   ```

4. **Create a minimal test:**
   ```bash
   python3 -c "
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       browser = p.chromium.launch(headless=True)
       page = browser.new_page()
       page.goto('https://example.com')
       print(f'Title: {page.title()}')
       browser.close()
   "
   ```

## Reporting Issues

When reporting issues, please include:
- Python version (`python3 --version`)
- Operating system and version
- Complete error message
- Output of `python3 validate_project.py`
- Installation method attempted
