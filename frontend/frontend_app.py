from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Render the home page (index.html) when accessing the root URL ('/').
    Returns:
        Response: The rendered HTML page (index.html).
    """
    return render_template("index.html")


if __name__ == '__main__':
    """
    Run the Flask application on the specified host and port in debug mode.
    """
    app.run(host="0.0.0.0", port=5001, debug=True)
