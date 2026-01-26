"""
Consolidated helpers module - Contains all utility functions previously scattered across utils/
This merges: auth.py, post_manager.py, project_manager.py, and pricing_manager.py
"""

import json
import os
import functools
from flask import session, redirect, url_for, flash, request
from typing import List, Dict, Optional

# =============================================================================
# AUTH FUNCTIONALITY (from utils/auth.py)
# =============================================================================

# Get admin credentials from environment variables or use defaults for development
# IMPORTANT: Set these as environment variables in production!
ADMIN_USERNAME = os.environ.get('BLOG_ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('BLOG_ADMIN_PASSWORD', 'your-secure-password-here')

def is_authenticated():
    """Check if the user is currently authenticated"""
    return session.get('authenticated', False)

def login(username, password):
    """Attempt to log in with the provided credentials"""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['authenticated'] = True
        return True
    return False

def logout():
    """Log out the current user"""
    session.pop('authenticated', None)

def login_required(view):
    """Decorator to require login for specific routes"""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not is_authenticated():
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

# =============================================================================
# POST MANAGEMENT (from utils/post_manager.py)
# =============================================================================

# Use robust path resolution - content/ folder is relative to project root
_APP_DIR = os.path.dirname(__file__)  # /path/to/app/
_PROJECT_ROOT = os.path.dirname(_APP_DIR)  # /path/to/PyArch.dev/
POSTS_FILE = os.path.join(_PROJECT_ROOT, 'content', 'posts.json')

def load_posts():
    """Load blog posts from JSON file"""
    with open(POSTS_FILE, 'r') as f:
        return json.load(f)
    
def save_posts(posts):
    """Save blog posts to JSON file"""
    with open(POSTS_FILE, "w") as f:
        json.dump(posts, f, indent=4)

# =============================================================================
# PROJECT MANAGEMENT (from utils/project_manager.py)
# =============================================================================

PROJECTS_FILE = os.path.join(_PROJECT_ROOT, 'content', 'projects.json')

def _ensure_projects_file():
    """Ensure projects file exists"""
    os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
    if not os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'w') as f:
            json.dump([], f)

def load_projects() -> List[Dict]:
    """Load projects from the JSON file."""
    _ensure_projects_file()
    with open(PROJECTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Alias for compatibility with existing imports
load_all_projects = load_projects

def save_projects(projects: List[Dict]) -> None:
    """Persist projects to the JSON file."""
    _ensure_projects_file()
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=4)

def get_project(slug: str) -> Optional[Dict]:
    """Get a single project by its slug/name."""
    projects = load_projects()
    return next((p for p in projects if p.get('slug') == slug), None)

# =============================================================================
# PRICING MANAGEMENT (from utils/pricing_manager.py)
# =============================================================================

PRICING_FILE = os.path.join(_PROJECT_ROOT, 'content', 'pricing.json')

def load_pricing_data():
    """Load pricing data from JSON file."""
    try:
        with open(PRICING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_service_info(service_key):
    """Get information for a specific service."""
    pricing_data = load_pricing_data()
    return pricing_data.get('services', {}).get(service_key, {})

def get_pricing_tiers():
    """Get all pricing tier information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('pricing_tiers', {})

def get_contact_info():
    """Get contact information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('contact', {})

def get_demo_info():
    """Get demo information."""
    pricing_data = load_pricing_data()
    return pricing_data.get('demo', {})

def get_performance_metrics():
    """Get performance metrics."""
    pricing_data = load_pricing_data()
    return pricing_data.get('performance_metrics', {})

def get_use_cases():
    """Get use cases."""
    pricing_data = load_pricing_data()
    return pricing_data.get('use_cases', [])
