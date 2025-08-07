#!/usr/bin/env python3
"""
Test runner for the Fantasy Hockey Flask application.
Runs all tests using Python's built-in unittest module.
"""

import sys
import unittest
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_all_tests():
    """Discover and run all tests."""
    # Discover all tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run the tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

def run_specific_test(test_module):
    """Run a specific test module."""
    try:
        # Import and run specific test module
        suite = unittest.TestLoader().loadTestsFromName(f'tests.{test_module}')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1
    except ImportError:
        print(f"Error: Could not import test module 'tests.{test_module}'")
        return 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test module
        test_module = sys.argv[1]
        exit_code = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all tests for Fantasy Hockey Flask application...")
        print("=" * 60)
        exit_code = run_all_tests()

    sys.exit(exit_code)
