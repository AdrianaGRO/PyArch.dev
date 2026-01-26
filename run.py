#!/usr/bin/env python3
"""
PyArch.dev Runner Script
Simple way to start the Flask application from project root
"""

import os
import sys

# Add the app directory to the Python path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    print("🚀 Starting PyArch.dev...")
    print("📁 Project structure: app/ | content/ | frontend/")
    print("🌐 Server will be available at: http://localhost:5003")
    print("=" * 50)
    app.run(debug=True, port=5003)
