# Masterblog API 📝

This project is a simple blogging platform built using Flask. It includes both an API for managing blog posts and a web interface for interacting with the blog posts. 

> *This project was developed as part of an assignment in the Software Engineer Bootcamp.* 🎓

## Features ✨
- **API**:
  - CRUD operations for blog posts (Create, Read, Update, Delete) 🔄.
  - Rate-limiting for API requests ⏱️.
  - CORS support to allow cross-origin requests 🌍.
  - Swagger UI for API documentation 📜.
- **Web Interface**:
  - A user-friendly interface to add, view, update, and delete blog posts.
  - Allows changing the base URL of the API and saving it for future use 🔗.

## Technologies 🛠️
- Flask (Python web framework)
- Flask-Limiter (API rate-limiting)
- Flask-CORS (Cross-Origin Resource Sharing)
- Flask-Swagger-UI (API documentation)
- HTML, CSS, JavaScript for the web interface

## Requirements 📋

- Python 3.x
- Flask
- Flask-Limiter
- Flask-CORS
- Flask-Swagger-UI
- Requests

## Installation ⚙️

### 1. Clone the repository:

```bash
git clone https://github.com/Ell-716/Masterblog-API.git
```
### 2. Install dependencies:

```bash
pip install -r requirements.txt
```
### 3. Running the application: 🚀
You can run the backend API server and web interface by executing the following command:

```bash
python backend_app.py  # For the API and backend (on port 5002)
python frontend_app.py  # For the frontend (on port 5001)
```
### 4. Access the API documentation: 📖
Once the Flask app is running, visit the following URL in your browser to view the Swagger UI for API documentation:

```bash
http://localhost:5002/api/docs
```
This will show all available API endpoints with interactive features for testing.

## API Endpoints 🌐

> GET /api/posts

- Retrieve a paginated and sorted list of blog posts.
- Query parameters:
  - ```sort```: Field to sort by (title, content, author, date).
  - ```direction```: Sort direction (asc or desc).
  - ```page```: Page number for pagination (default is 1).
  - ```limit```: Number of posts per page (default is 5).

> POST /api/posts

- Create a new blog post.
- Required fields in the request body:
  - ```title```: Title of the post.
  - ```content```: Content of the post.
  - ```author```: Author of the post.
  - ```date```: (Optional) Date of the post, defaults to today's date.

> PUT /api/posts/<id>

- Update an existing post by ID.
- Can update the ```title```, ```content```, and ```author```.

> DELETE /api/posts/<id>

- Delete a blog post by ID.

> GET /api/posts/search

- Search for posts by ```title```, ```content```, ```author```, or ```date```.

## Web Interface 🛜

- **Homepage**: Allows you to view all blog posts and interact with the API using buttons to update or delete posts.
- **Add New Post**: Fill out the form to add a new blog post to the platform.

### Settings 

- You can configure the API base URL using the input field at the top. The URL will be saved in your browser's local storage so you don't have to re-enter it every time.

## Rate Limiting ⏰

The API implements rate limiting for requests to prevent abuse:

- ```GET /api/posts```: Limited to 10 requests per minute.
- ```POST /api/posts```: Limited to 5 requests per minute.
- ```DELETE /api/posts/<id>```: Limited to 3 requests per minute.
- ```PUT /api/posts/<id>```: Limited to 5 requests per minute.

If you exceed the rate limits, the API will return a ```429 Too Many Requests``` response with an error message.

## Notes 🗒️

- The blog posts are stored in a ```posts.json``` file.
- In production, you may want to replace the JSON file with a proper database.

## Contributing 🤝

Feel free to fork the repository, submit issues, or create pull requests. Contributions are welcome!
