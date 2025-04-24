from flask import Flask, render_template, url_for
# url_for is used in base.html to generate URLs for static files

from game_logic import print_question, get_available_questions, read_question, lifeline
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route handler for the home page.

    Args:
        None

    Returns:
        A rendered HTML template for the index page.
        And displays a question from the available questions.
    """
    old_questions = set()
    all_questions = read_question()

    while True:
        available = get_available_questions(all_questions, old_questions)
        
        if not available:
            print("\nThere's no questions left. Add more! And you win i guess?")
            break

        current_entry = random.choice(available)
        old_questions.add(current_entry["ID"])
        question = print_question(current_entry)
        life = lifeline()

    return render_template('index.html', question = question, lifeline = life)


if __name__ == "__main__":
    app.run(debug=True)