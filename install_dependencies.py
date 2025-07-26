#!/usr/bin/env python3
"""Alternative installation script to handle Python 3.13 compatibility issues."""

import subprocess
import sys
import os


def run_command(command, description, ignore_errors=False):
    """Run a command and handle errors.
    
    Args:
        command: Command to run as a list
        description: Description of what the command does
        ignore_errors: Whether to continue if command fails
    """
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr.strip():
            print(f"   Error: {e.stderr.strip()}")
        if not ignore_errors:
            return False
        else:
            print("   Continuing despite error...")
            return True
    except FileNotFoundError:
        print(f"❌ Command not found: {' '.join(command)}")
        return False


def check_python_version():
    """Check Python version and provide guidance."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13+ detected - using compatibility installation method")
        return "python313"
    elif version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return "compatible"
    else:
        print("❌ Python 3.8+ required")
        return "incompatible"


def install_for_python313():
    """Install dependencies for Python 3.13+ with compatibility workarounds."""
    print("\n🔧 Installing dependencies for Python 3.13+")
    print("=" * 50)
    
    # Install basic dependencies first
    commands = [
        ([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
         "Upgrading pip"),
        ([sys.executable, "-m", "pip", "install", "pytest>=7.4.0"], 
         "Installing pytest"),
        ([sys.executable, "-m", "pip", "install", "python-dotenv>=1.0.0"], 
         "Installing python-dotenv"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    # Try to install playwright with binary-only option
    playwright_commands = [
        ([sys.executable, "-m", "pip", "install", "playwright", "--only-binary=all"], 
         "Installing Playwright (binary only)"),
        ([sys.executable, "-m", "pip", "install", "pytest-playwright", "--only-binary=all"], 
         "Installing pytest-playwright (binary only)"),
    ]
    
    playwright_success = False
    for command, description in playwright_commands:
        if run_command(command, description, ignore_errors=True):
            playwright_success = True
        else:
            print(f"   Trying alternative installation method...")
            # Try without --only-binary flag
            alt_command = command[:-1]  # Remove --only-binary=all
            if run_command(alt_command, f"{description} (alternative method)", ignore_errors=True):
                playwright_success = True
    
    if not playwright_success:
        print("\n⚠️  Playwright installation failed. Manual installation required:")
        print("   Try one of these methods:")
        print("   1. conda install -c conda-forge playwright")
        print("   2. pip install playwright --pre")
        print("   3. Use Python 3.11 or 3.12 instead")
        return False
    
    # Install optional dependencies
    optional_commands = [
        ([sys.executable, "-m", "pip", "install", "pytest-html"], 
         "Installing pytest-html (optional)"),
        ([sys.executable, "-m", "pip", "install", "pytest-xdist"], 
         "Installing pytest-xdist (optional)"),
    ]
    
    for command, description in optional_commands:
        run_command(command, description, ignore_errors=True)
    
    return True


def install_for_compatible_python():
    """Install dependencies for Python 3.8-3.12."""
    print("\n🔧 Installing dependencies for compatible Python version")
    print("=" * 50)
    
    commands = [
        ([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
         "Upgrading pip"),
        ([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
         "Installing all dependencies from requirements.txt"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def install_playwright_browsers():
    """Install Playwright browsers."""
    return run_command(
        [sys.executable, "-m", "playwright", "install"],
        "Installing Playwright browsers"
    )


def verify_installation():
    """Verify the installation."""
    print("\n🔍 Verifying installation...")
    
    # Test imports
    test_imports = [
        ("pytest", "pytest"),
        ("playwright.sync_api", "Playwright"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_good = True
    for module, package in test_imports:
        try:
            __import__(module)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            all_good = False
    
    return all_good


def main():
    """Main installation function."""
    print("🚀 Playwright Python Dependencies Installer")
    print("=" * 50)
    
    # Check Python version
    python_status = check_python_version()
    
    if python_status == "incompatible":
        print("\n❌ Please upgrade to Python 3.8 or higher")
        return 1
    
    # Install dependencies based on Python version
    if python_status == "python313":
        success = install_for_python313()
    else:
        success = install_for_compatible_python()
    
    if not success:
        print("\n❌ Dependency installation failed")
        return 1
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        print("\n⚠️  Playwright browsers installation failed")
        print("   Try running manually: playwright install")
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run validation: python3 validate_project.py")
        print("   2. Run tests: python3 run_tests.py")
        return 0
    else:
        print("\n⚠️  Installation completed but verification found issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
