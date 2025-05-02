from flask import Flask, render_template, request, redirect, url_for, session, flash, json
import random
from flask import session

app = Flask(__name__)
app.secret_key = 'dev'

def load_questions(filename='questions.json'):
    """
    This function reads a JSON file and returns the data as a list.
    If the file is not found, print an error message.
        Args:
            None
        Returns:
            A list of questions from the JSON file.
    """

    try:
        with open(filename, 'r') as file:
            questions = json.load(file)
            return questions
    except FileNotFoundError:
        print("Error: questions.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: JSON file is malformed.")
        return []
    
QUESTIONS = load_questions('questions.json')

def get_session_list(key):
    """Retrieve a value from the session by key."""
    return session.get(key)

def set_session_list(key, value):
    """Set a value in the session for the given key."""
    session[key] = value

def init_session(category):
    """Initialize the session with a selected category and clear all previous data."""
    session.clear()
    session['category'] = category

@app.route('/', methods=['GET', 'POST'])
def index():
    """Function to render index.html and allow users to select a desired caregory of questions"""
    if request.method == 'POST':
        category = request.form.get('category')
        init_session(category)
        return redirect(url_for('question'))

    categories = ['all'] + sorted({question['category'] for question in QUESTIONS}, key=str.lower)

    return render_template('index.html', categories=categories)


@app.route('/question', methods=['GET', 'POST'])
def question():
    """Main game function so far only renders a question and added check if available but timeline not implemented so it wont do anything"""
    if request.method == 'POST':

        current_id = session.get('current_id')

        next_question = next((question for question in QUESTIONS if question['ID'] == current_id))

    available = [question for question in QUESTIONS if question['ID'] not in session.get('old_questions', []) and (session['category'] == 'all' or question['category'].lower()==session['category'].lower())]

    next_question = random.choice(available)
    session['current_id'] = next_question['ID']

    return render_template('question.html', next_question = next_question)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
