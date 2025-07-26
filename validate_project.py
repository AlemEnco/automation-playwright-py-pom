#!/usr/bin/env python3
"""Project validation script to check structure and syntax."""

import os
import sys
import ast
import importlib.util
from pathlib import Path


def validate_python_syntax(file_path):
    """Validate Python file syntax.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to check syntax
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_project_structure():
    """Check if all required project files and directories exist."""
    required_structure = {
        'files': [
            'requirements.txt',
            'pytest.ini',
            'playwright.config.py',
            'README.md',
            '.env'
        ],
        'directories': [
            'pages',
            'tests',
            'utils',
            'reports',
            'logs'
        ],
        'python_files': [
            'pages/__init__.py',
            'pages/base_page.py',
            'pages/login_page.py',
            'pages/dashboard_page.py',
            'tests/__init__.py',
            'tests/conftest.py',
            'tests/test_login.py',
            'utils/__init__.py',
            'utils/test_data.py'
        ]
    }
    
    missing_items = []
    
    # Check files
    for file_path in required_structure['files']:
        if not os.path.exists(file_path):
            missing_items.append(f"Missing file: {file_path}")
    
    # Check directories
    for dir_path in required_structure['directories']:
        if not os.path.isdir(dir_path):
            missing_items.append(f"Missing directory: {dir_path}")
    
    # Check Python files
    for py_file in required_structure['python_files']:
        if not os.path.exists(py_file):
            missing_items.append(f"Missing Python file: {py_file}")
    
    return missing_items


def validate_python_files():
    """Validate syntax of all Python files in the project."""
    python_files = []
    
    # Find all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    validation_results = []
    
    for py_file in python_files:
        is_valid, error = validate_python_syntax(py_file)
        validation_results.append({
            'file': py_file,
            'valid': is_valid,
            'error': error
        })
    
    return validation_results


def check_imports():
    """Check if critical imports can be resolved."""
    import_tests = [
        ('pages.base_page', 'BasePage'),
        ('pages.login_page', 'LoginPage'),
        ('pages.dashboard_page', 'DashboardPage'),
        ('utils.test_data', 'TestDataManager'),
    ]
    
    import_results = []
    
    for module_name, class_name in import_tests:
        try:
            # Add current directory to path
            sys.path.insert(0, '.')
            
            # Try to import the module
            spec = importlib.util.spec_from_file_location(
                module_name, 
                module_name.replace('.', '/') + '.py'
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if class exists
                if hasattr(module, class_name):
                    import_results.append({
                        'module': module_name,
                        'class': class_name,
                        'success': True,
                        'error': None
                    })
                else:
                    import_results.append({
                        'module': module_name,
                        'class': class_name,
                        'success': False,
                        'error': f"Class {class_name} not found in module"
                    })
            else:
                import_results.append({
                    'module': module_name,
                    'class': class_name,
                    'success': False,
                    'error': "Module spec could not be created"
                })
                
        except Exception as e:
            import_results.append({
                'module': module_name,
                'class': class_name,
                'success': False,
                'error': str(e)
            })
    
    return import_results


def main():
    """Main validation function."""
    print("🔍 Validating Playwright Python Test Automation Project")
    print("=" * 60)
    
    # Check project structure
    print("\n📁 Checking project structure...")
    missing_items = check_project_structure()
    
    if missing_items:
        print("❌ Missing items found:")
        for item in missing_items:
            print(f"   - {item}")
    else:
        print("✅ All required files and directories are present")
    
    # Validate Python syntax
    print("\n🐍 Validating Python file syntax...")
    validation_results = validate_python_files()
    
    syntax_errors = [r for r in validation_results if not r['valid']]
    
    if syntax_errors:
        print("❌ Syntax errors found:")
        for result in syntax_errors:
            print(f"   - {result['file']}: {result['error']}")
    else:
        print("✅ All Python files have valid syntax")
    
    # Check imports
    print("\n📦 Checking critical imports...")
    import_results = check_imports()
    
    import_errors = [r for r in import_results if not r['success']]
    
    if import_errors:
        print("❌ Import errors found:")
        for result in import_errors:
            print(f"   - {result['module']}.{result['class']}: {result['error']}")
    else:
        print("✅ All critical imports are working")
    
    # Summary
    print("\n📊 Validation Summary")
    print("-" * 30)
    
    total_issues = len(missing_items) + len(syntax_errors) + len(import_errors)
    
    if total_issues == 0:
        print("🎉 Project validation PASSED! All checks successful.")
        print("\n📋 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Install Playwright browsers: playwright install")
        print("   3. Run tests: pytest")
        return 0
    else:
        print(f"⚠️  Project validation found {total_issues} issues that need to be fixed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
