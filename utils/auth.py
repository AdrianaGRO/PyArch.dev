import os
import functools
from flask import session, redirect, url_for, flash, request

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
