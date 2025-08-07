from flask import Flask, render_template, request, redirect, url_for, flash
from utils.post_manager import load_posts, save_posts 
from datetime import datetime
import markdown
import re
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
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
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<id>')
def post(id):
    posts = load_posts()
    post = next((p for p in posts if str(p['id']) == str(id)),None)
    if post is None:
        return "<h1>Post not found</h1>", 404
    return render_template('post.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        
        # Handle image upload if present
        if 'image' in request.files and request.files['image'].filename:
            image_path = handle_image_upload(request.files['image'])
            if image_path:
                # Insert the image Markdown at the cursor position or append to content
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
        return redirect(url_for("index"))
    return render_template('create_post.html')        

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
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
        return redirect(url_for('post', id=post['id']))
    return render_template('edit_post.html', post=post)



@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    posts = load_posts()
    posts = [p for p in posts if str(p['id']) != str(id)]
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)