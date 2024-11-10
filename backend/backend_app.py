from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    errors = {}

    # Check if 'title' and 'content' are provided
    if "title" not in data:
        errors["title"] = "Title is required."
    elif not data["title"].strip():
        errors["title"] = "Title cannot be empty."
    elif len(data["title"]) > 100:
        errors["title"] = "Title cannot exceed 100 characters."

    if "content" not in data:
        errors["content"] = "Content is required."
    elif not data["content"].strip():
        errors["content"] = "Content cannot be empty."
    elif len(data["content"]) > 1000:
        errors["content"] = "Content cannot exceed 1000 characters."

    # If there are any errors, return the errors dictionary; otherwise, return None
    if errors:
        return errors
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    new_post = request.get_json()

    # Validate the new post data
    validation_errors = validate_post_data(new_post)
    if validation_errors:
        return jsonify({"error": "Invalid post data", "details": validation_errors}), 400

    # Generate a unique ID for the new post
    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
