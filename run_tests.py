#!/usr/bin/env python3
"""Test runner script for the Playwright Python test automation project."""

import subprocess
import sys
import argparse
import os
from datetime import datetime


def run_pytest_command(args_list, description):
    """Run pytest with given arguments.
    
    Args:
        args_list: List of pytest arguments
        description: Description of the test run
    """
    print(f"🧪 {description}")
    print(f"Command: pytest {' '.join(args_list)}")
    print("-" * 60)
    
    try:
        # Run pytest
        result = subprocess.run([sys.executable, "-m", "pytest"] + args_list, 
                              check=False)
        
        print("-" * 60)
        if result.returncode == 0:
            print(f"✅ {description} - All tests passed!")
        else:
            print(f"❌ {description} - Some tests failed (exit code: {result.returncode})")
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install dependencies first:")
        print("   python setup.py")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Playwright Python tests")
    parser.add_argument("--smoke", action="store_true", 
                       help="Run smoke tests only")
    parser.add_argument("--login", action="store_true", 
                       help="Run login tests only")
    parser.add_argument("--ui", action="store_true", 
                       help="Run UI tests only")
    parser.add_argument("--regression", action="store_true", 
                       help="Run regression tests only")
    parser.add_argument("--headless", action="store_true", 
                       help="Run tests in headless mode")
    parser.add_argument("--parallel", action="store_true", 
                       help="Run tests in parallel")
    parser.add_argument("--html-report", action="store_true", 
                       help="Generate HTML report")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--test-file", type=str, 
                       help="Run specific test file")
    parser.add_argument("--test-function", type=str, 
                       help="Run specific test function")
    
    args = parser.parse_args()
    
    # Build pytest arguments
    pytest_args = []
    
    # Add markers
    if args.smoke:
        pytest_args.extend(["-m", "smoke"])
    elif args.login:
        pytest_args.extend(["-m", "login"])
    elif args.ui:
        pytest_args.extend(["-m", "ui"])
    elif args.regression:
        pytest_args.extend(["-m", "regression"])
    
    # Add specific test file or function
    if args.test_file:
        pytest_args.append(args.test_file)
    if args.test_function:
        pytest_args.extend(["-k", args.test_function])
    
    # Add browser options
    if args.headless:
        # For headless mode, we don't add --headed flag (default is headless)
        pass
    else:
        # For headed mode, add the --headed flag
        pytest_args.append("--headed")
    
    # Add parallel execution
    if args.parallel:
        pytest_args.extend(["-n", "auto"])
    
    # Add HTML report
    if args.html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/test_report_{timestamp}.html"
        pytest_args.extend(["--html", report_file, "--self-contained-html"])
    
    # Add verbose output
    if args.verbose:
        pytest_args.append("-v")
    
    # Default arguments if none specified
    if not pytest_args:
        pytest_args = ["-v"]
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Determine test description
    if args.smoke:
        description = "Running smoke tests"
    elif args.login:
        description = "Running login tests"
    elif args.ui:
        description = "Running UI tests"
    elif args.regression:
        description = "Running regression tests"
    elif args.test_file:
        description = f"Running tests from {args.test_file}"
    elif args.test_function:
        description = f"Running test function: {args.test_function}"
    else:
        description = "Running all tests"
    
    # Run the tests
    return run_pytest_command(pytest_args, description)


if __name__ == "__main__":
    print("🎯 Playwright Python Test Runner")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("tests") or not os.path.exists("pages"):
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected directories: tests/, pages/")
        sys.exit(1)
    
    exit_code = main()
    
    print("\n" + "=" * 40)
    if exit_code == 0:
        print("🎉 Test execution completed successfully!")
    else:
        print("⚠️  Test execution completed with issues")
    
    sys.exit(exit_code)
