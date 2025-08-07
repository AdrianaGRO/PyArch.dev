import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'posts.json')

def load_posts():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
    
def save_posts(posts):
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=4)

