
from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.post_manager import load_posts, save_posts
from utils.auth import login, logout, login_required, is_authenticated
from datetime import datetime
import markdown
import re
import os
import uuid
from urllib.parse import quote_plus
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# New imports for Projects section
from utils.project_manager import load_projects as load_all_projects, get_project
from utils.pricing_manager import load_pricing_data, get_pricing_tiers, get_contact_info
from jinja2 import TemplateNotFound

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


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

@app.route('/')
def index():
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
def blog():
    """Dedicated blog page - all posts"""
    posts = load_posts()
    # Sort posts by date, newest first
    posts_sorted = sorted(
        posts, 
        key=lambda x: x.get('created_at', ''), 
        reverse=True
    )
    return render_template('blog.html', posts=posts_sorted)

@app.route('/about')
def about():
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
def contact():
    return render_template('contact.html')

@app.route('/post/<id>')
def post(id):
    """Individual blog post page"""
    posts = load_posts()
    post = next((p for p in posts if str(p['id']) == str(id)), None)
    if post is None:
        return "<h1>Post not found</h1>", 404
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
def projects_index():
    """Projects listing page"""
    projects = load_all_projects()
    return render_template('projects/index.html', projects=projects)

@app.route('/projects/<project_name>')
def project_detail(project_name):
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
def pricing():
    """Pricing and demo page for Data Cleaner tool"""
    pricing_data = load_pricing_data()
    return render_template('pricing.html', pricing_data=pricing_data)


if __name__ == '__main__':
    app.run(debug=True, port=5003)