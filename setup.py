#!/usr/bin/env python3
"""Setup script for the Playwright Python test automation project."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors.
    
    Args:
        command: Command to run as a list
        description: Description of what the command does
    """
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {' '.join(command)}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Playwright requires Python 3.8 or higher")
        return False


def install_dependencies():
    """Install Python dependencies using the compatibility installer."""
    print("🔧 Using compatibility installer for dependencies...")
    try:
        result = subprocess.run([sys.executable, "install_dependencies.py"],
                              check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("❌ Compatibility installer failed")
        print("💡 Try manual installation:")
        print("   python3 install_dependencies.py")
        return False
    except FileNotFoundError:
        print("❌ install_dependencies.py not found")
        return False


def install_playwright_browsers():
    """Install Playwright browsers."""
    return run_command(
        [sys.executable, "-m", "playwright", "install"],
        "Installing Playwright browsers"
    )


def create_directories():
    """Create necessary directories."""
    directories = ["reports", "logs", "reports/screenshots", "reports/videos"]
    
    print("📁 Creating necessary directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}")
    
    print("✅ Directories created successfully")
    return True


def verify_installation():
    """Verify the installation by running the validation script."""
    print("🔍 Verifying installation...")
    try:
        result = subprocess.run([sys.executable, "validate_project.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Playwright Python Test Automation Project")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create directories
    if not create_directories():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        print("💡 Try running manually:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        print("\n❌ Failed to install Playwright browsers")
        print("💡 Try running manually:")
        print("   playwright install")
        return 1
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run all tests: pytest")
        print("   2. Run smoke tests: pytest -m smoke")
        print("   3. Run login tests: pytest -m login")
        print("   4. Generate HTML report: pytest --html=reports/report.html")
        return 0
    else:
        print("\n⚠️  Setup completed but verification found issues")
        print("💡 Check the validation output above for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
