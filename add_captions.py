import json
import os

# Set the correct working directory
os.chdir('/Users/adricati/Personal Development/PyArch.dev')

# Load the posts
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

# Update the first post content with resized images and captions
if posts:
    content = posts[0]['content']
    
    # Replace the first image with HTML that includes width and caption
    content = content.replace(
        '<img src="/static/uploads/stock/python-journey.jpg" alt="My Python Journey" width="600" class="blog-image">',
        '<img src="/static/uploads/stock/python-journey.jpg" alt="My Python Journey" width="600" class="blog-image">\n<p class="image-caption">Starting my Python coding journey</p>'
    )
    
    # Replace the second image with HTML that includes width and caption
    content = content.replace(
        '<img src="/static/uploads/stock/coding-laptop.jpg" alt="Coding on laptop" width="500" class="blog-image">',
        '<img src="/static/uploads/stock/coding-laptop.jpg" alt="Coding on laptop" width="500" class="blog-image">\n<p class="image-caption">Finding motivation in problem-solving</p>'
    )
    
    # Replace the third image with HTML that includes width and caption
    content = content.replace(
        '<img src="/static/uploads/stock/learning-process.jpg" alt="Learning process" width="550" class="blog-image">',
        '<img src="/static/uploads/stock/learning-process.jpg" alt="Learning process" width="550" class="blog-image">\n<p class="image-caption">The ongoing journey of learning and documentation</p>'
    )
    
    # Update the post
    posts[0]['content'] = content
    
    # Save back to the file
    with open('data/posts.json', 'w') as f:
        json.dump(posts, f, indent=4)
    
    print("Captions added to images in your blog post!")
else:
    print("No posts found.")
