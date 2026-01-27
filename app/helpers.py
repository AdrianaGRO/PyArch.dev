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
    """Load blog posts from JSON file, filtering out unpublished posts"""
    with open(POSTS_FILE, 'r') as f:
        all_posts = json.load(f)
    
    # Filter out unpublished posts for public display
    published_posts = [post for post in all_posts if post.get('published', True)]
    return published_posts
    
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

# =============================================================================
# FLASK STATIC FILE DEBUGGING UTILITIES
# =============================================================================

def debug_static_configuration(app=None):
    """
    Debug Flask static file configuration and print comprehensive diagnostics.
    Call this in your app.py to troubleshoot static file issues.
    
    Usage: debug_static_configuration(app)
    """
    if app is None:
        from flask import current_app as app
    
    print("=" * 60)
    print("FLASK STATIC FILE DEBUGGING")
    print("=" * 60)
    
    # Basic Flask configuration
    print(f"App name: {app.name}")
    print(f"App root path: {app.root_path}")
    print(f"Static folder: {app.static_folder}")
    print(f"Static URL path: {app.static_url_path}")
    print(f"Template folder: {app.template_folder}")
    
    # Check if static folder exists
    if app.static_folder and os.path.exists(app.static_folder):
        print(f"✓ Static folder exists: {app.static_folder}")
        
        # List contents of static folder
        try:
            static_contents = os.listdir(app.static_folder)
            print(f"Static folder contents: {static_contents}")
            
            # Check for common image directories
            for img_dir in ['images', 'img', 'pictures', 'assets', 'projects']:
                img_path = os.path.join(app.static_folder, img_dir)
                if os.path.exists(img_path):
                    print(f"✓ Image directory exists: {img_path}")
                    try:
                        img_files = os.listdir(img_path)
                        print(f"  Files in {img_dir}/: {img_files}")
                    except Exception as e:
                        print(f"  Error listing {img_dir}/: {e}")
                else:
                    print(f"✗ Image directory missing: {img_path}")
                    
        except Exception as e:
            print(f"✗ Error accessing static folder: {e}")
    else:
        print(f"✗ Static folder missing or invalid: {app.static_folder}")
    
    print("=" * 60)

def validate_image_path(image_path, app=None):
    """
    Validate if an image path exists in the static folder.
    
    Args:
        image_path (str): Path like "/static/images/logo.png" or "images/logo.png"
        app: Flask app instance (optional)
    
    Returns:
        dict: Validation results with status and suggestions
    """
    if app is None:
        from flask import current_app as app
    
    result = {
        'valid': False,
        'exists': False,
        'full_path': None,
        'suggestions': []
    }
    
    # Clean the image path
    clean_path = image_path.lstrip('/')
    if clean_path.startswith('static/'):
        clean_path = clean_path[7:]  # Remove 'static/' prefix
    
    # Build full filesystem path
    full_path = os.path.join(app.static_folder, clean_path)
    result['full_path'] = full_path
    
    # Check if file exists
    if os.path.exists(full_path):
        result['valid'] = True
        result['exists'] = True
    else:
        result['suggestions'].append(f"File not found: {full_path}")
        
        # Check case sensitivity issues
        dir_path = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        
        if os.path.exists(dir_path):
            try:
                actual_files = os.listdir(dir_path)
                # Look for case-insensitive matches
                for actual_file in actual_files:
                    if actual_file.lower() == filename.lower():
                        result['suggestions'].append(f"Case mismatch found: {actual_file} vs {filename}")
                        break
                else:
                    result['suggestions'].append(f"Available files in directory: {actual_files}")
            except Exception as e:
                result['suggestions'].append(f"Error checking directory: {e}")
        else:
            result['suggestions'].append(f"Directory doesn't exist: {dir_path}")
    
    return result

def generate_correct_image_urls():
    """
    Generate examples of correct image URL usage in Flask templates.
    Returns a dictionary with various scenarios.
    """
    examples = {
        'basic_static_image': {
            'template_code': '{{ url_for("static", filename="images/logo.png") }}',
            'description': 'Basic static image in images/ folder',
            'html_example': '<img src="{{ url_for(\'static\', filename=\'images/logo.png\') }}" alt="Logo">'
        },
        'project_image': {
            'template_code': '{{ url_for("static", filename="projects/data_cleaner.png") }}',
            'description': 'Project-specific image',
            'html_example': '<img src="{{ url_for(\'static\', filename=\'projects/data_cleaner.png\') }}" alt="Data Cleaner">'
        },
        'dynamic_project_image': {
            'template_code': '{% if project.hero_image %}\n{{ url_for("static", filename=project.hero_image.lstrip("/static/")) }}\n{% endif %}',
            'description': 'Dynamic project image with path cleaning',
            'html_example': '{% if project.hero_image %}\n<img src="{{ url_for(\'static\', filename=project.hero_image.lstrip(\'/static/\')) }}" alt="{{ project.title }}">\n{% endif %}'
        },
        'upload_image': {
            'template_code': '{{ url_for("static", filename="uploads/" + image_filename) }}',
            'description': 'User-uploaded image',
            'html_example': '<img src="{{ url_for(\'static\', filename=\'uploads/\' + image_filename) }}" alt="Upload">'
        }
    }
    return examples

def check_common_image_issues(app=None):
    """
    Check for common Flask static image issues and provide solutions.
    
    Returns:
        dict: Issues found and recommendations
    """
    if app is None:
        from flask import current_app as app
    
    issues = []
    recommendations = []
    
    # Check 1: Static folder configuration
    if not app.static_folder:
        issues.append("No static folder configured")
        recommendations.append("Set app.static_folder = 'path/to/static'")
    elif not os.path.exists(app.static_folder):
        issues.append(f"Static folder doesn't exist: {app.static_folder}")
        recommendations.append(f"Create directory: {app.static_folder}")
    
    # Check 2: Static URL path
    if app.static_url_path != '/static':
        issues.append(f"Non-standard static URL path: {app.static_url_path}")
        recommendations.append("Consider using default '/static' path")
    
    # Check 3: Common image directories
    if app.static_folder and os.path.exists(app.static_folder):
        expected_dirs = ['images', 'img', 'projects', 'uploads']
        for dir_name in expected_dirs:
            dir_path = os.path.join(app.static_folder, dir_name)
            if not os.path.exists(dir_path):
                recommendations.append(f"Consider creating: {dir_path}")
    
    # Check 4: File permissions (on Unix systems)
    if app.static_folder and os.path.exists(app.static_folder):
        try:
            test_read = os.access(app.static_folder, os.R_OK)
            if not test_read:
                issues.append("No read permission on static folder")
                recommendations.append("Check file permissions on static directory")
        except Exception:
            pass  # Skip permission check on Windows
    
    return {
        'issues': issues,
        'recommendations': recommendations,
        'status': 'healthy' if not issues else 'needs_attention'
    }
