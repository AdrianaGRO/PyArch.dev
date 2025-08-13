import json
import os

# Set the correct working directory
os.chdir('/Users/adricati/Personal Development/PyArch.dev')

# Load the posts
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

# Update the first post content with resized images
if posts:
    content = posts[0]['content']
    
    # Replace the first image with HTML that includes width
    content = content.replace(
        '![My Python Journey](/static/uploads/stock/python-journey.jpg)',
        '<img src="/static/uploads/stock/python-journey.jpg" alt="My Python Journey" width="600" class="blog-image">'
    )
    
    # Replace the second image with HTML that includes width
    content = content.replace(
        '![Coding on laptop](/static/uploads/stock/coding-laptop.jpg)',
        '<img src="/static/uploads/stock/coding-laptop.jpg" alt="Coding on laptop" width="500" class="blog-image">'
    )
    
    # Replace the third image with HTML that includes width
    content = content.replace(
        '![Learning process](/static/uploads/stock/learning-process.jpg)',
        '<img src="/static/uploads/stock/learning-process.jpg" alt="Learning process" width="550" class="blog-image">'
    )
    
    # Update the post
    posts[0]['content'] = content
    
    # Save back to the file
    with open('data/posts.json', 'w') as f:
        json.dump(posts, f, indent=4)
    
    print("Images resized in your blog post!")
else:
    print("No posts found.")
