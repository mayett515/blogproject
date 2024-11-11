# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_blog_posts():
    """Load blog posts from JSON file."""
    json_path = os.path.join('data', 'blog_post.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty list if file doesn't exist yet
        return []


@app.route('/')
def index():
    """Display all blog posts on the home page."""
    loaded_json_blog_posts = load_blog_posts()
    blog_posts = loaded_json_blog_posts['posts']
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')

    elif request.method == 'POST':
        new_post = {
            'author': request.form.get('author', ''),
            'title': request.form.get('title', ''),
            'content': request.form.get('content', '')
        }

        blog_data = load_blog_posts()
        blog_posts = blog_data.get('posts', [])

        if blog_posts:
            new_post['id'] = max(post['id'] for post in blog_posts) + 1
        else:
            new_post['id'] = 1

        blog_posts.append(new_post)

        with open(os.path.join('data', 'blog_post.json'), 'w') as f:
            json.dump({'posts': blog_posts}, f, indent=4)

        return redirect(url_for('index'))


@app.route('/delete/<int:post_id>')
def delete(post_id):
    try:
        # Load existing posts
        with open(os.path.join('data', 'blog_post.json'), 'r') as f:
            data = json.load(f)

        # Filter out the post with the given id
        data['posts'] = [post for post in data['posts'] if post['id'] != post_id]

        # Save the updated posts back to the file
        with open(os.path.join('data', 'blog_post.json'), 'w') as f:
            json.dump(data, f, indent=4)

    except FileNotFoundError:
        # Handle case where file doesn't exist
        pass

    # Redirect back to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)