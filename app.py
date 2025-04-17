from flask import Flask, render_template, url_for
# url_for is used in base.html to generate URLs for static files

from game_logic import print_question, get_available_questions, read_question

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
    old_questions = set()
    all_questions = read_question() 
    current_entry = get_available_questions(all_questions, old_questions)
    return render_template('index.html', available_question = print_question(current_entry))


if __name__ == "__main__":
    app.run(debug=True)