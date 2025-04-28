from flask import Flask, render_template, url_for
# url_for is used in base.html to generate URLs for static files

from game_logic import print_question, get_available_questions, read_question, lifeline
import random

app = Flask(__name__)

def print_a_question_from_file():
    """
    Selects and returns a random available question from a file.

    Reads all questions from a file, filters out questions that have already been asked,
    and randomly selects one from the remaining available questions. If no questions are available,
    a message is printed to inform the user. The selected question's ID is added to the set of
    previously asked questions to avoid repetition.

    Returns:
        str: The text of the selected question.
    """
    old_questions = set()
    all_questions = read_question()
    
    available = get_available_questions(all_questions, old_questions)
        
    if not available:
        print("\nThere's no questions left. Add more! And you win i guess?")

    current_entry = random.choice(available)
    old_questions.add(current_entry["ID"])
    return current_entry["question"]

@app.route('/', methods=['GET'])
def index():
    """
    Route handler for the home page.

    Args:
        None

    Returns:
        A rendered HTML template for the index page.
        And displays a question from the available questions.
    """
    question = print_a_question_from_file()

    return render_template('index.html', question = question)


if __name__ == "__main__":
    app.run(debug=True)