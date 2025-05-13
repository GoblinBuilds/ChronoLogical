from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import psycopg2

app = Flask(__name__)
app.secret_key = 'dev'


def load_questions(table_name='questions'):
    """
    Fetches all rows from the specified table in the PostgreSQL database.
    If the database connection fails, it returns an empty list.
    
    Args:
        table_name (str): The name of the table to fetch questions from.
    
    Returns:
        list: A list of questions from the database.
    """
    try:
         # Hardcoded database connection details
        conn = psycopg2.connect(
            dbname="aq3524",
            user="aq3524",
            password="abc123",
            host="pgserver.mau.se",
            port="5432"
        )
        cursor = conn.cursor()
        # Dynamically query the specified table
        query = f"SELECT question_id, date, question, category FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert rows to a list of dictionaries
        questions = [
            {"question_id": row[0], "date": row[1], "question": row[2], "category": row[3]}
            for row in rows
        ]
        return questions
    except Exception as e:
        print(f"Error: {e}")
        return []
    
# # Example usage
# if __name__ == "__main__":
#     questions = load_questions('questions')
#     print(questions)

QUESTIONS = load_questions('questions')

def get_session_list(key):
    """Retrieve a value from the session by key."""
    return session.get(key)

def set_session_list(key, value):
    """Set a value in the session for the given key."""
    session[key] = value

def init_session(category):
    """Initialize the session with a selected category and clear all previous data."""
    session.clear()
    session['categories'] = category
    session['unlocked'] = []
    session['locked'] = []
    session['lifeline_count'] = 0
    session['old_questions'] = []
    session['stage'] = 1 
    session['score'] = 000 

    available_questions = [question for question in QUESTIONS if question['category'] in category]

    if available_questions:
        random_question = random.choice(available_questions)
        session['locked'] = [random_question]
        # session['old_questions'] = [random_question['question_id']]
    else:
        flash("No questions available in the selected category. Please select a different category.")

@app.route('/', methods=['GET', 'POST'])
def index():
    """Function to render index.html and allow users to select a desired caregory of questions."""
    if request.method == 'POST':
        category_list = request.form.getlist('category')
        if not category_list:
            flash("Please select at least one category.")
            return redirect(url_for('index'))
        """category = [cat for cat in category_list if cat["category"] in category_list]"""
        init_session(category_list)
        return redirect(url_for('game'))

    categories = sorted({question['category'] for question in QUESTIONS}, key = str.lower)
    return render_template('index.html', categories = categories)


@app.route('/game', methods=['GET', 'POST'])
def game():
    """Main route for the game logic.
        Presents player with questions one after another when player does a input.
        Handles player input: 
        Players can: 
            'place' to place a questionin relation to the timeline throug inputing a value representing a index.
            'lock' to lock their current timeline. This action decrease a lifeline.
            'quit' to return to the index.

            When a question is answered through 'place' or if the timeline is locked the question is added to a list tracking what questions have already been shown
            prevening it from appering several times.
        Renders game.html template
    """
    if request.method == 'POST':
        action = request.form.get('action')
        current_id = session.get('current_id')

        next_question = next((question for question in QUESTIONS if question['question_id'] == current_id))
        timeline = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])

        if action == 'quit':
            session.clear()
            return redirect(url_for('index'))

        if action == 'lock':
            if session.get('unlocked'):
                session['locked'] = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])
                session['unlocked'] = []
                session['lifeline_count'] = session.get('lifeline_count', 0) + 1
                lives_left = 3 - session['lifeline_count']
                flash('The timeline is locked!')
                if lives_left > 0:
                    flash(f'You have {lives_left} life(s) left.')
                else:
                    session.clear()
                    return redirect(url_for('index'))
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
                else:
                    session['lifeline_count'] = session.get('lifeline_count', 0) + 1
                    session['unlocked'] = []
                    lives_left = 3 - session['lifeline_count']

                    if lives_left > 0:
                        flash(f'Wrong placement! You have {lives_left} life(s) left.')
                    else:
                        session.clear()
                        return redirect(url_for('index'))
                    
            if len(session.get('unlocked', [])) + len(session.get('locked', [])) == 5:
                flash("Congratulations! You've Won!")
                # session.clear()
                return redirect(url_for('win_screen'))
        
        if action in ('place', 'lock') and current_id:
            old = session.get('old_questions', [])
            old.append(current_id)
            session['old_questions'] = old

        return redirect(url_for('game'))

    selected = session.get('categories', [])
    available = [question for question in QUESTIONS if question['question_id'] not in session.get('old_questions', []) and (question['category'] in selected)]
    if not available:
        flash("There's no more questions available!")
        return redirect(url_for('index'))

    next_question = random.choice(available)
    song_embed_url = None  

    if next_question["category"] == "Song":
        song_url = next_question["question"]
        if "/track/" in song_url:
            try:
                track_id = song_url.split("/track/")[1].split("?")[0]
                song_embed_url = f"https://open.spotify.com/embed/track/{track_id}"
                # next_question["question"] = "Guess the year of this song!"
            except IndexError:
                song_embed_url = None  
        else:
            song_embed_url = None 

    session['current_id'] = next_question['question_id']
    timeline = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])

    locked = session.get('locked', [])
    unlocked = session.get('unlocked', [])
    score = session.get('score', [])

    return render_template('game.html', next_question=next_question, song_embed_url=song_embed_url, locked=locked, unlocked=unlocked, score=score, max_index=len(timeline))

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
    """This function renders win_screen.html. Actions POST in the HTML-file are:
    - continue: continue the game to the next stage.
    - restart: restart the game.
    """
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'continue':
            old_questions = session.get('old_questions', [])
            score = session.get('score', 0)
            stage = session.get('stage', 1)

            session['unlocked'] = []
            session['locked'] = []
            session['lifeline_count'] = 0 

            session['stage'] = stage + 1

            session['old_questions'] = old_questions  
            session['score'] = score 

            return redirect(url_for('game')) 

        elif action == 'restart':
            return redirect(url_for('index'))  
    
    return render_template('win_screen.html')


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
