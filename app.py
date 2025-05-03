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
    session['unlocked'] = []
    session['locked'] = []
    session['lifeline_count'] = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    """Function to render index.html and allow users to select a desired caregory of questions"""
    if request.method == 'POST':
        category = request.form.get('category')
        init_session(category)
        return redirect(url_for('game'))

    categories = ['all'] + sorted({question['category'] for question in QUESTIONS}, key = str.lower)
    return render_template('index.html', categories = categories)


@app.route('/game', methods=['GET', 'POST'])
def game():
    """Main route for the game logic.
        Presents player with questions one after another when player does a input
        Handles player input 
        Players can: 
            'place' to place a questionin relation to the timeline throug inputing a value representing a index
            'lock' to lock their current timelin
            'quit' to return to the index 

        Renders game.html template
    """
    if request.method == 'POST':
        action = request.form.get('action')
        current_id = session.get('current_id')

        next_question = next((question for question in QUESTIONS if question['ID'] == current_id))
        timeline = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])

        if action == 'quit':
            session.clear()
            return redirect(url_for('index'))

        if action == 'lock':
            if session.get('unlocked'):
                session['locked'] = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])
                session['unlocked'] = []
                flash('Tidslinjen låst!')

            else:
                flash('Inget att låsa.')


        if action == 'place':
            input_index = int(request.form.get('index', -1))
            if 0 <= input_index <= len(timeline):
                valid_placement = check_valid_placement(timeline, next_question, input_index)

                if valid_placement:
                    session['unlocked'] = sorted(session.get('unlocked', []) + [next_question], key=lambda e: e['date'])
                    flash('Rätt placering!')

                else:
                    session['lifeline_count'] = session.get('lifeline_count', 0) + 1
                    session['unlocked'] = []
                    lives_left = 3 - session['lifeline_count']

                    if lives_left > 0:
                        flash(f'Fel placering! Du har {lives_left} liv kvar.')

                    else:
                        session.clear()
                        return redirect(url_for('index'))
                    
            else:
                flash('Ogiltigt index.')

        return redirect(url_for('game'))

    available = [question for question in QUESTIONS if question['ID'] and (session['category'] == 'all' or question['category'].lower() == session['category'].lower())]
    if not available:
        flash('Inga fler frågor kvar!')
        session.clear()
        return redirect(url_for('index'))

    next_question = random.choice(available)
    session['current_id'] = next_question['ID']
    timeline = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])
    locked_dates = [entry['date'] for entry in session.get('locked', [])]
    unlocked_dates = [entry['date'] for entry in session.get('unlocked', [])]

    return render_template('game.html', next_question = next_question, locked = locked_dates, unlocked = unlocked_dates, max_index = len(timeline))

def check_valid_placement(combined_timeline, next_question, index):
    """
    Checks if a new next_question can be placed at the specified index in the list,
    based on the date value of the next_question and the surrounding elements in the list. It checks:

    - If the list is empty: its is considered valid.
    - If the index is 0: the next_question's date must be less than or equal to the date of the first element.
    - If the index is at the end of the list: the next_question date must be greater than or equal to the date of the last element.
    - If the index is in the middle of the list: the next_question date must be between the dates surrounding elements.

    Args:
        combined_timeline (list): A list of dictionaries, checks values at date.
        next_question (dict): The new next_question to be placed.
        index (int): The user input index  to check if the next_question can be placed at that index.

    Returns:
        bool: True if the next_question can be validly placed at the user selected index otherwise False.
    """
    timeline = combined_timeline
    input_index = index

    valid = False
    question_date = next_question['date']
    if len(timeline) == 0:
        valid = True
    elif input_index == 0:
        valid = question_date <= timeline[0]['date']
    elif input_index == len(timeline):
        valid = question_date >= timeline[-1]['date']
    else:
        valid = timeline[input_index-1]['date'] <= question_date <= timeline[input_index]['date']

    return valid

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
