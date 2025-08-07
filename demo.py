#!/usr/bin/env python3
"""
Demo script for the Fantasy Hockey Flask application.
Demonstrates testing capabilities and basic functionality.
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and display the result."""
    print(f"\n{'='*60}")
    print(f"🏒 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}")
    print("-" * 40)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ SUCCESS")
        if result.stdout.strip():
            print(result.stdout)
    else:
        print("❌ FAILED")
        if result.stderr.strip():
            print(result.stderr)

    return result.returncode == 0

def main():
    """Run the demonstration."""
    print("🏒 Fantasy Hockey Platform - Testing Demo")
    print("==========================================")

    # Test the application structure
    success = True

    # 1. Run the test suite
    success &= run_command(
        "python run_tests.py",
        "Running comprehensive test suite (29 tests)"
    )

    # 2. Test API endpoints (if app is running)
    print(f"\n{'='*60}")
    print("🏒 API Testing Demo")
    print(f"{'='*60}")
    print("Note: Start the Flask app with 'python app.py' to test API endpoints")
    print("Example API calls you can test:")
    print("  curl http://localhost:5000/players/api")
    print("  curl http://localhost:5000/teams/api")
    print("  curl http://localhost:5000/leagues/api")

    # 3. Show database structure
    success &= run_command(
        "python -c \"from flaskr.db import get_db; from flaskr import create_app; app = create_app({'TESTING': True, 'DATABASE': 'instance/hockey.sqlite'}); ctx = app.app_context(); ctx.push(); db = get_db(); cursor = db.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\\\"table\\\"'); tables = cursor.fetchall(); print('\\nDatabase Tables:'); [print(f'  - {table[0]}') for table in tables]; ctx.pop()\"",
        "Checking database structure"
    )

    # 4. Show test coverage by module
    success &= run_command(
        "python -c \"import os; print('\\nTest Files:'); [print(f'  - {f}') for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')]\"",
        "Listing available test modules"
    )

    print(f"\n{'='*60}")
    if success:
        print("🎉 Demo completed successfully!")
        print("Your fantasy hockey platform is ready for development!")
    else:
        print("⚠️  Some parts of the demo had issues.")
        print("Check the error messages above for details.")

    print(f"{'='*60}")
    print("\n📚 Next steps:")
    print("  1. Run 'python app.py' to start the web server")
    print("  2. Visit http://localhost:5000 to explore the app")
    print("  3. Run 'python run_tests.py' anytime to verify functionality")
    print("  4. Add your own tests in the tests/ directory")

if __name__ == '__main__':
    main()
