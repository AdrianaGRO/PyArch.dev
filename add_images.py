import json
import os

# Set the correct working directory
os.chdir('/Users/adricati/Personal Development/PyArch.dev')

# Load the posts
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

# Update the first post content with images
if posts:
    # Add images to appropriate sections in the content
    content = posts[0]['content']
    
    # Add header image after the title
    header_image = "\n\n![My Python Journey](/static/uploads/stock/python-journey.jpg)\n\n"
    content = content.split("This is it. My first real blog post about learning Python.")
    content = content[0] + "This is it. My first real blog post about learning Python." + header_image + content[1]
    
    # Add a second image in the middle
    second_image = "\n\n![Coding on laptop](/static/uploads/stock/coding-laptop.jpg)\n\n"
    if "## Why I'm Really Doing This" in content:
        parts = content.split("## Why I'm Really Doing This")
        content = parts[0] + second_image + "## Why I'm Really Doing This" + parts[1]
    
    # Add a third image near the end
    third_image = "\n\n![Learning process](/static/uploads/stock/learning-process.jpg)\n\n"
    if "## What This Blog Will Actually Cover" in content:
        parts = content.split("## What This Blog Will Actually Cover")
        content = parts[0] + third_image + "## What This Blog Will Actually Cover" + parts[1]
    
    # Update the post
    posts[0]['content'] = content
    
    # Save back to the file
    with open('data/posts.json', 'w') as f:
        json.dump(posts, f, indent=4)
    
    print("Images added to your blog post!")
else:
    print("No posts found.")
