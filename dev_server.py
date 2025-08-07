#!/usr/bin/env python3
"""
Development server script for the Fantasy Hockey Flask application.
Provides enhanced development features including auto-browser launch and live reload.
"""

import os
import sys
import argparse
import webbrowser
import threading
import time
from flaskr import create_app

def open_browser(url):
    """Open the default web browser to the specified URL after a short delay."""
    time.sleep(1.5)  # Wait for Flask to start up
    print(f"🌐 Opening browser to {url}")
    webbrowser.open(url)

def main():
    parser = argparse.ArgumentParser(description='Run the Fantasy Hockey Flask development server')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the server on (default: 5000)')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t automatically open browser')
    parser.add_argument('--no-reload', action='store_true', help='Disable live reload')
    parser.add_argument('--production', action='store_true', help='Run in production mode (no debug)')

    args = parser.parse_args()

    # Create the app
    app = create_app()

    # Set up URL
    url = f"http://{args.host}:{args.port}"

    # Configure based on arguments
    debug_mode = not args.production
    reload_enabled = not args.no_reload and debug_mode

    print("🏒 Fantasy Hockey Platform - Development Server")
    print("=" * 50)
    print(f"🚀 Starting server at {url}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    print(f"🔄 Live reload: {'ON' if reload_enabled else 'OFF'}")
    print(f"🌐 Auto-browser: {'ON' if not args.no_browser and debug_mode else 'OFF'}")
    print("=" * 50)

    if debug_mode:
        print("💡 Development features enabled:")
        print("   - Automatic restarts when files change")
        print("   - Interactive debugger on errors")
        print("   - Detailed error pages")

        if not args.no_browser:
            print("   - Auto-browser launch")

        print("\n📝 Available endpoints:")
        print("   - Home:     /")
        print("   - Players:  /players/")
        print("   - Teams:    /teams/")
        print("   - Leagues:  /leagues/")
        print("   - API:      /players/api, /teams/api, /leagues/api")
        print(f"\n🛑 Press Ctrl+C to stop the server")
        print("=" * 50)

    # Open browser automatically in development mode
    if debug_mode and not args.no_browser:
        threading.Timer(1, open_browser, args=(url,)).start()

    try:
        # Run the server
        app.run(
            debug=debug_mode,
            port=args.port,
            host=args.host,
            use_reloader=reload_enabled,
            use_debugger=debug_mode,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
