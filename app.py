from flask import Flask, render_template, url_for
# url_for is used in base.html to generate URLs for static files

from game_logic import print_question, get_available_questions, read_question, lifeline
import random

app = Flask(__name__)

@app.route('/')
def index():
    """
    Route handler for the home page.

    Args:
        None

    Returns:
        A rendered HTML template for the index page.
        And displays a question from the available questions.
    """
    read_question()
    old_questions = set()
    all_questions = read_question()

    available = get_available_questions(all_questions, old_questions)
    current_entry = random.choice(available)
    old_questions.add(current_entry["ID"])
    return render_template('index.html', question = print_question(current_entry), lifeline = lifeline())


if __name__ == "__main__":
    app.run(debug=True)