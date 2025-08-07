#!/usr/bin/env python3
"""
Setup script for the Fantasy Hockey Flask application.
This script will initialize the database and populate it with test data.
"""

import os
import sys
import subprocess

def setup_app():
    print("Setting up Fantasy Hockey Flask Application...")

    # Set the Flask app environment variable
    os.environ['FLASK_APP'] = 'flaskr'

    # Initialize the database
    print("Initializing database...")
    result = subprocess.run(['flask', 'init-db'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error initializing database: {result.stderr}")
        return False
    print("Database initialized successfully!")

    # Populate with test data
    print("Populating database with test data...")
    result = subprocess.run([sys.executable, 'populate_test_data.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error populating test data: {result.stderr}")
        return False
    print("Test data populated successfully!")

    print("\nSetup complete! You can now run the application with:")
    print("  python app.py")
    print("  or")
    print("  flask run")
    print("\nThe application will be available at http://localhost:5000")

    return True

if __name__ == '__main__':
    success = setup_app()
    if not success:
        sys.exit(1)
