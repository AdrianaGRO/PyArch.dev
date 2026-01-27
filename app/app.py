from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_babel import Babel, gettext as _, lazy_gettext as _l
from helpers import (
    # Auth functions
    login, logout, login_required, is_authenticated,
    # Post management
    load_posts, save_posts,
    # Project management
    load_all_projects, get_project,
    # Pricing management
    load_pricing_data, get_pricing_tiers, get_contact_info
)
from datetime import datetime
import markdown
import re
import os
import uuid
from urllib.parse import quote_plus
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from jinja2 import TemplateNotFound

# Load environment variables from .env file
load_dotenv()

# Define paths relative to project root
_APP_DIR = os.path.dirname(os.path.abspath(__file__))  # /path/to/app/
_PROJECT_ROOT = os.path.dirname(_APP_DIR)  # /path/to/PyArch.dev/
_FRONTEND_DIR = os.path.join(_PROJECT_ROOT, 'frontend')
_TEMPLATE_DIR = os.path.join(_FRONTEND_DIR, 'templates')

# Debug: Print paths on startup
print(f"APP_DIR: {_APP_DIR}")
print(f"PROJECT_ROOT: {_PROJECT_ROOT}")
print(f"TEMPLATE_DIR: {_TEMPLATE_DIR}")
print(f"Template exists: {os.path.exists(os.path.join(_TEMPLATE_DIR, 'index.html'))}")

# Initialize Flask with correct template and static paths
app = Flask(__name__,
           template_folder=_TEMPLATE_DIR,
           static_folder=os.path.join(_FRONTEND_DIR, 'static'))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = os.path.join(_FRONTEND_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Configure Babel for internationalization
def get_locale():
    '''Determine the user's preferred language - TEMPORARILY ENGLISH ONLY'''
    # TEMPORARY: Default to English only for quality assurance
    # Will reactivate multilingual support when native translations are ready
    return 'en'
    
    # COMMENTED OUT - Original multilingual logic:
    # # 1. Check if language is in URL path
    # if request.view_args and 'lang' in request.view_args:
    #     lang = request.view_args['lang']
    #     if lang in ['en', 'ro', 'es']:
    #         session['language'] = lang
    #         return lang
    # 
    # # 2. Check if language is stored in session
    # if 'language' in session:
    #     return session['language']
    # 
    # # 3. Fall back to browser language preference
    # return request.accept_languages.best_match(['en', 'ro', 'es']) or 'en'

# Initialize Babel (single initialization)
babel = Babel(app, locale_selector=get_locale)

# Babel configuration
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(_PROJECT_ROOT, 'tools', 'translations')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

# TEMPORARY: Only English available for quality assurance
# Will restore full language support when native translations are ready
app.config['LANGUAGES'] = {
    'en': {'name': 'English', 'flag': '🇺🇸'},
    # 'ro': {'name': 'Română', 'flag': '🇷🇴'},  # Temporarily disabled - pending native level review
    # 'es': {'name': 'Español', 'flag': '🇪🇸'}   # Temporarily disabled - pending native level review
}


# Custom Jinja filter for markdown processing
@app.template_filter('md')
def md_filter(text):
    if not text:
        return ""
    # Process markdown
    md_html = markdown.markdown(
        text,
        extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables', 'markdown.extensions.nl2br']
    )
    # Replace double line breaks with paragraphs for better spacing
    md_html = re.sub(r'<br />\s*<br />', '</p><p>', md_html)
    # Wrap content in paragraphs if not already
    if not md_html.startswith('<'):
        md_html = f'<p>{md_html}</p>'
    return md_html

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def handle_image_upload(file):
    """Process uploaded image and return the path to be used in Markdown"""
    if not file:
        return None
        
    if file and allowed_file(file.filename):
        # Create a unique filename to prevent conflicts
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Create the uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Return the path relative to the static folder for use in Markdown
        return f"/static/uploads/{unique_filename}"
    
    return None

@app.before_request
def before_request():
    '''Set current language before each request'''
    g.current_lang = get_locale()

@app.context_processor
def inject_conf_var():
    '''Make configuration variables available to all templates'''
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        current_lang=g.get('current_lang', 'en')
    )

@app.template_filter('reject_lang')
def reject_lang_filter(view_args):
    '''Remove lang parameter from view_args for cleaner URLs'''
    if view_args is None:
        return {}
    return {k: v for k, v in view_args.items() if k != 'lang'}

@app.route('/')
@app.route('/<lang>/')
def index(lang='en'):
    """Homepage - Shows hero, services, projects, and blog posts"""
    posts = load_posts()
    projects = load_all_projects()
    
    # Get featured project
    featured_project = next(
        (p for p in projects if p.get('featured')), 
        projects[0] if projects else None
    )
    
    # Sort posts by date, newest first
    posts_sorted = sorted(
        posts, 
        key=lambda x: x.get('created_at', ''), 
        reverse=True
    )
    
    return render_template(
        'index.html', 
        posts=posts_sorted,
        projects=projects,
        featured_project=featured_project
    )

@app.route('/blog')
@app.route('/<lang>/blog')
def blog(lang='en'):
    """Dedicated blog page - all posts"""
    posts = load_posts()
    
    # Normalize posts to ensure consistent field names
    for post in posts:
        # Use 'date' if available, otherwise fall back to 'created_at'
        if 'date' in post and not post.get('created_at'):
            post['created_at'] = post['date']
        elif not post.get('created_at') and not post.get('date'):
            post['created_at'] = '2026-01-22'  # Default date
    
    # Sort posts by date, newest first
    posts_sorted = sorted(
        posts, 
        key=lambda x: x.get('created_at', ''), 
        reverse=True
    )
    return render_template('blog.html', posts=posts_sorted)

@app.route('/about')
@app.route('/<lang>/about')
def about(lang='en'):
    """About page - Shows personal story with recent projects and posts"""
    posts = load_posts()
    projects = load_all_projects()
    
    # Get 3 most recent posts for sidebar
    recent_posts = sorted(
        posts, 
        key=lambda x: x.get('created_at', ''), 
        reverse=True
    )[:3] if posts else []
    
    return render_template(
        'about.html', 
        recent_posts=recent_posts, 
        projects=projects
    )

@app.route('/contact')
@app.route('/<lang>/contact')
def contact(lang='en'):
    return render_template('contact.html')

@app.route('/post/<id>')
def post(id):
    """Individual blog post page"""
    posts = load_posts()
    post = next((p for p in posts if str(p['id']) == str(id)), None)
    if post is None:
        return "<h1>Post not found</h1>", 404
    
    # Convert markdown content to HTML
    if 'content' in post:
        post['content_html'] = markdown.markdown(post['content'])
    
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new blog post (admin only)"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        
        # Handle image upload 
        if 'image' in request.files and request.files['image'].filename:
            image_path = handle_image_upload(request.files['image'])
            if image_path:
                # Insert the image Markdown 
                image_md = f"\n\n![{title}]({image_path})\n\n"
                content += image_md
        
        posts = load_posts()
        new_id = max([post['id'] for post in posts], default=0) + 1
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        posts.append({
            'id': new_id,
            'title': title,
            'content': content,
            'category': category,
            'created_at': created_at
        })
        save_posts(posts)
        flash('Post created successfully!', 'success')
        return redirect(url_for("index"))
    return render_template('create_post.html')        

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing blog post (admin only)"""
    posts = load_posts()
    post = next((p for p in posts if str(p['id']) == str(id)), None) 
    if not post:
        return "<h1>Post not found</h1>", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        post['category'] = request.form.get('category', '')
        
        # Handle image upload if present
        if 'image' in request.files and request.files['image'].filename:
            image_path = handle_image_upload(request.files['image'])
            if image_path:
                # Insert the image Markdown at the end of content
                image_md = f"\n\n![{post['title']}]({image_path})\n\n"
                post['content'] += image_md
        
        save_posts(posts)
        flash('Post updated successfully!', 'success')
        return redirect(url_for('post', id=post['id']))
    return render_template('edit_post.html', post=post)



@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    """Delete blog post (admin only)"""
    posts = load_posts()
    posts = [p for p in posts if str(p['id']) != str(id)]
    save_posts(posts)
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page for admin access"""
    if is_authenticated():
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if login(username, password):
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):  # Only redirect to relative URLs
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')


@app.route('/logout')
def logout_page():
    """Logout and return to homepage"""
    logout()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


@app.route('/projects')
@app.route('/<lang>/projects')
def projects_index(lang='en'):
    """Projects listing page"""
    projects = load_all_projects()
    return render_template('projects/index.html', projects=projects)

@app.route('/projects/<project_name>')
@app.route('/<lang>/projects/<project_name>')
def project_detail(project_name, lang='en'):
    """Project detail page with template fallback"""
    project = get_project(project_name)
    if not project:
        return "<h1>Project not found</h1>", 404
    
    try:
        # Try to render specific project template first
        return render_template(f"projects/{project_name}.html", project=project)
    except TemplateNotFound:
        # Fall back to generic project detail template
        return render_template("projects/detail.html", project=project)


@app.route('/pricing')
@app.route('/<lang>/pricing')
def pricing(lang='en'):
    """Pricing and demo page for Data Cleaner tool"""
    pricing_data = load_pricing_data()
    return render_template('pricing.html', pricing_data=pricing_data)

# Add this route for debugging static files during development
@app.route('/debug/static')
def debug_static():
    """Debug endpoint to check static file configuration"""
    if not app.debug:
        return "Debug mode only", 403
    
    from helpers import debug_static_configuration, check_common_image_issues
    
    # Create debug output
    import io
    import sys
    from contextlib import redirect_stdout
    
    output = io.StringIO()
    with redirect_stdout(output):
        debug_static_configuration(app)
        print("\n")
        issues = check_common_image_issues(app)
        print("Issues report:", issues)
    
    debug_text = output.getvalue()
    
    # Return as HTML with preformatted text
    return f"<html><body><pre>{debug_text}</pre></body></html>"

if __name__ == '__main__':
    app.run(debug=True, port=5003)