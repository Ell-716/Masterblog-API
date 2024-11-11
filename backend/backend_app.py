import datetime
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Swagger configuration
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Masterblog API'}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Initialize Limiter
limiter = Limiter(get_remote_address, app=app)


def load_posts():
    """
    Loads the blog posts from the JSON file.
    Returns:
        list: A list of blog post dictionaries from the JSON file.
    """
    try:
        with open("posts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"posts.json not found: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data in posts.json: {e}")
        return []


def save_posts(posts):
    """
    Saves the blog posts to the JSON file.
    Args:
        posts (list): A list of blog post dictionaries to save.
    """
    try:
        with open("posts.json", "w", encoding="utf-8") as file:
            json.dump(posts, file, indent=4)
    except IOError as e:
        print(f"File write error: {e}")
    except TypeError as e:
        print(f"Data serialization error: {e}")
    except ValueError as e:
        print(f"JSON encoding error: {e}")


def validate_post_data(data, partial=False):
    validation_errors = []

    # Validate only provided fields if partial=True
    if 'author' in data and (not isinstance(data['author'], str) or not data['author'].strip()):
        validation_errors.append('Author must be a non-empty string.')
    elif 'author' not in data and not partial:
        validation_errors.append("Author is required.")

    if 'title' in data and (not isinstance(data['title'], str) or not data['title'].strip()):
        validation_errors.append('Title must be a non-empty string.')
    elif 'title' not in data and not partial:
        validation_errors.append("Title is required.")

    if 'content' in data and (not isinstance(data['content'], str) or not data['content'].strip()):
        validation_errors.append('Content must be a non-empty string.')
    elif 'content' not in data and not partial:
        validation_errors.append("Content is required.")

    if 'date' in data and (not isinstance(data['date'], str) or not data['date'].strip()):
        validation_errors.append('Date must be a valid string.')
    elif 'date' not in data and not partial:
        validation_errors.append("Date is required.")

    return validation_errors if validation_errors else None


@app.route('/api/posts', methods=['GET'])
@limiter.limit("10/minute")
def get_posts():
    """
    Retrieve a paginated and sorted list of blog posts.
    Query Params:
        sort (str): Field to sort by ('title', 'content', 'author', 'date').
        direction (str): Sort direction ('asc' or 'desc').
        page (int): Page number for pagination (default is 1).
        limit (int): Number of posts per page (default is 5).
    """
    blog_posts = load_posts()
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    # Sort validation
    if sort and sort not in ['title', 'content', 'author', 'date']:
        return jsonify({"error": "Invalid sort field. Must be 'title', 'content', 'author' or 'date'."}), 400
    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    # Apply sorting
    sorted_posts = sorted(blog_posts, key=lambda post: post.get(sort, ""),
                          reverse=(direction == 'desc')) if sort else blog_posts

    # Pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = sorted_posts[start_index:end_index]

    return jsonify(paginated_posts)


@app.route('/api/posts', methods=['POST'])
@limiter.limit("5/minute")
def add_post():
    """
    Create a new blog post with the provided data.
    """
    blog_posts = load_posts()
    new_post = request.get_json()
    new_post["date"] = new_post.get("date", datetime.date.today().strftime("%Y-%m-%d"))

    validation_errors = validate_post_data(new_post)
    if validation_errors:
        return jsonify({"error": "Invalid post data", "details": validation_errors}), 400

    new_id = max((post["id"] for post in blog_posts), default=0) + 1
    new_post["id"] = new_id
    blog_posts.append(new_post)
    save_posts(blog_posts)
    return jsonify(new_post), 201


def find_post_by_id(blog_posts, post_id):
    """
    Find a post by its ID.
    """
    return next((post for post in blog_posts if post['id'] == post_id), None)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@limiter.limit("3/minute")
def delete_post(id):
    """
    Delete a blog post by ID.
    """
    blog_posts = load_posts()
    post = find_post_by_id(blog_posts, id)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    blog_posts = [post for post in blog_posts if post["id"] != id]
    save_posts(blog_posts)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
@limiter.limit("5/minute")
def update_post(id):
    """
    Update a blog post by ID with provided data.
    """
    blog_posts = load_posts()
    post = find_post_by_id(blog_posts, id)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"error": "No data provided for update"}), 400

    # Validate only fields present in the updated_data
    validation_errors = validate_post_data(updated_data, partial=True)
    if validation_errors:
        return jsonify({"error": "Invalid post data", "details": validation_errors}), 400

    # Update only the fields present in the request data
    for key, value in updated_data.items():
        post[key] = value

    save_posts(blog_posts)
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
@limiter.limit("10/minute")
def search_post():
    """
    Search for blog posts by title, content, author, or date.
    Query Params:
        title (str): Keyword in the title.
        content (str): Keyword in the content.
        author (str): Keyword in the author.
        date (str): Exact match on the date.
    """
    blog_posts = load_posts()
    search_posts = []

    title = request.args.get('title')
    content = request.args.get('content')
    author = request.args.get('author')
    date = request.args.get('date')

    for post in blog_posts:
        if (
            (title and title.lower() in post['title'].lower()) or
            (content and content.lower() in post['content'].lower()) or
            (author and author.lower() in post['author'].lower()) or
            (date and date == post['date'])  # exact match for date
        ):
            search_posts.append(post)

    return jsonify(search_posts)


@app.errorhandler(429)
def rate_limit_exceeded(e):
    """
    Custom error handler for rate limit exceeded.
    """
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
