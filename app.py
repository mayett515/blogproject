# app.py
from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def load_blog_posts():
    """Load blog posts from JSON file."""
    json_path = os.path.join('data', 'blog_posts.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty list if file doesn't exist yet
        return []

@app.route('/')
def index():
    """Display all blog posts on the home page."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(debug=True)