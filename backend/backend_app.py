import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Initialize Limiter
limiter = Limiter(get_remote_address, app=app)

POSTS = [
    {
        "id": 1,
        "title": "First post",
        "content": "This is the first post.",
        "author": "Your Name",
        "date": "2023-06-07"
    },
    {
        "id": 2,
        "title": "Second post",
        "content": "This is the second post.",
        "author": "Your Name",
        "date": "2023-06-08"
    },
]


def validate_post_data(data):
    errors = {}

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

    if "author" not in data:
        errors["author"] = "Author is required."
    elif not data["author"].strip():
        errors["author"] = "Author cannot be empty."

    if errors:
        return errors
    return None


@app.route('/api/posts', methods=['GET'])
@limiter.limit("10/minute")  # Limit to 10 requests per minute
def get_posts():
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if sort and sort not in ['title', 'content', 'author', 'date']:
        return jsonify({"error": "Invalid sort field. Must be 'title', 'content', 'author' or 'date'."}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    # Handle pagination parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    # First, apply sorting if sort and direction are provided
    sorted_posts = POSTS
    if sort:
        sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=(direction == 'desc'))

    # Then, apply pagination to the sorted posts
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = sorted_posts[start_index:end_index]

    # Return the paginated and optionally sorted posts
    return jsonify(paginated_posts)


@app.route('/api/posts', methods=['POST'])
@limiter.limit("10/minute")
def add_post():
    new_post = request.get_json()

    # If 'date' is not provided, set it to today's date
    if "date" not in new_post or not new_post["date"].strip():
        new_post["date"] = datetime.date.today().strftime("%Y-%m-%d")

    validation_errors = validate_post_data(new_post)
    if validation_errors:
        return jsonify({"error": "Invalid post data", "details": validation_errors}), 400

    # Generate a unique ID for the new post
    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    POSTS.append(new_post)
    return jsonify(new_post), 201


def find_post_by_id(post_id):
    return next((post for post in POSTS if post['id'] == post_id), None)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@limiter.limit("10/minute")
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    # Remove the post with the specified id
    POSTS[:] = [post for post in POSTS if post['id'] != id]

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
@limiter.limit("10/minute")
def update_post(id):
    post = find_post_by_id(id)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    updated_post = request.get_json()

    if updated_post is None:
        return jsonify({"error": "Invalid post data"}), 400

    # Update only the fields that are provided, keep the current values for missing fields
    if "title" in updated_post:
        post['title'] = updated_post['title']
    if "content" in updated_post:
        post['content'] = updated_post['content']
    if "author" in updated_post:
        post['author'] = updated_post['author']
    if "date" in updated_post:
        post['date'] = updated_post['date']

    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
@limiter.limit("10/minute")
def search_post():
    search_posts = []

    title = request.args.get('title')
    content = request.args.get('content')
    author = request.args.get('author')
    date = request.args.get('date')

    for post in POSTS:
        if title and title.lower() in post['title'].lower():
            search_posts.append(post)
        elif content and content.lower() in post['content'].lower():
            search_posts.append(post)
        elif author and author.lower() in post['author'].lower():
            search_posts.append(post)
        elif date and date.lower() in post['date'].lower():
            search_posts.append(post)

    return jsonify(search_posts)


@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
