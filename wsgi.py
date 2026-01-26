"""
WSGI entry point for production deployment
This file is used by Gunicorn and other WSGI servers
"""

import os
import sys

# Add the app directory to Python path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
sys.path.insert(0, app_dir)

# Import the Flask application
from app import app

# WSGI callable
application = app

if __name__ == "__main__":
    app.run()
