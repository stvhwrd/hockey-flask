# Fantasy Hockey Flask App - Main entry point
import os
import webbrowser
import threading
import time
from flaskr import create_app

def open_browser():
    """Open the default web browser to the Flask app after a short delay."""
    time.sleep(1.5)  # Wait for Flask to start up
    webbrowser.open('http://localhost:5000')

# Create the app using the factory pattern
app = create_app()

if __name__ == '__main__':
    # Open browser automatically in development mode
    if app.debug:
        threading.Timer(1, open_browser).start()

    # Run with live reload enabled (debug=True enables automatic reloading)
    app.run(
        debug=True,
        port=5000,
        host='127.0.0.1',
        use_reloader=True,  # Enable live reload on file changes
        use_debugger=True,  # Enable interactive debugger
        threaded=True       # Handle multiple requests simultaneously
    )