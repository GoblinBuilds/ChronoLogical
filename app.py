from flask import Flask, render_template, url_for
# url_for is used in base.html to generate URLs for static files

from game_logic import *

app = Flask(__name__)

@app.route('/')
def index():
    """
    Route handler for the home page.

    Args:
        None

    Returns:
        A rendered HTML template for the index page.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)