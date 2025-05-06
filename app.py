from flask import Flask, render_template, request, redirect, url_for, session, flash, json
import random

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
    session['old_questions'] = []

    available_questions = [question for question in QUESTIONS if category == 'all' or question['category'].lower() == category.lower()]

    if available_questions:
        random_question = random.choice(available_questions)
        session['locked'] = [random_question]
        session['old_questions'] = [random_question['ID']]

@app.route('/', methods=['GET', 'POST'])
def index():
    """Function to render index.html and allow users to select a desired caregory of questions."""
    if request.method == 'POST':
        category = request.form.get('category')
        init_session(category)
        return redirect(url_for('game'))

    categories = ['all'] + sorted({question['category'] for question in QUESTIONS}, key = str.lower)
    return render_template('index.html', categories = categories)


@app.route('/game', methods=['GET', 'POST'])
def game():
    """Main route for the game logic.
        Presents player with questions one after another when player does a input.
        Handles player input: 
        Players can: 
            'place' to place a questionin relation to the timeline throug inputing a value representing a index.
            'lock' to lock their current timeline.
            'quit' to return to the index.

            When a question is answered through 'place' or if the timeline is locked the question is added to a list tracking what questions have already been shown
            prevening it from appering several times.
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
                flash('The timeline is locked!')
            else:
                flash("There's nothing to lock.")

        if action == 'place':
            user_input = request.form.get('index', -1)
            input_index = int(user_input) if user_input.isdigit() else -1
            if input_index == -1:
                flash('Invalid action.')
                return redirect(url_for('game'))
            if 0 <= input_index <= len(timeline):
                valid_placement = check_valid_placement(timeline, next_question, input_index)
                if valid_placement:
                    session['unlocked'] = sorted(session.get('unlocked', []) + [next_question], key=lambda e: e['date'])
                    flash('Correct placement!')
                else:
                    session['lifeline_count'] = session.get('lifeline_count', 0) + 1
                    session['unlocked'] = []
                    lives_left = 3 - session['lifeline_count']

                    if lives_left > 0:
                        flash(f'Wrong placement! You have {lives_left} life(s) left.')
                    else:
                        session.clear()
                        return redirect(url_for('index'))
                    
            if len(session.get('unlocked', [])) + len(session.get('locked', [])) == 10:
                flash("Congratulations! You've Won!")
                session.clear()
                return redirect(url_for('win_screen'))
        
        if action in ('place', 'lock') and current_id:
            old = session.get('old_questions', [])
            old.append(current_id)
            session['old_questions'] = old

        return redirect(url_for('game'))

    available = [question for question in QUESTIONS if question['ID'] not in session.get('old_questions', []) and (session['category'] == 'all' or question['category'].lower() == session['category'].lower())]
    if not available:
        flash("There's no more questions available!")
        session.clear()
        return redirect(url_for('index'))

    next_question = random.choice(available)
    session['current_id'] = next_question['ID']
    timeline = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])

    locked = session.get('locked', [])
    unlocked = session.get('unlocked', [])

    return render_template('game.html', next_question=next_question, locked=locked, unlocked=unlocked, max_index=len(timeline))

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

@app.route('/win_screen', methods=['GET', 'POST'])
def win_screen():
    """Function to render win_screen.html."""
    return render_template('win_screen.html')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
