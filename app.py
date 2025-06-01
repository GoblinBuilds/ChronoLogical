from flask import Flask, render_template, request, redirect, url_for, session, flash, json, jsonify
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
         # Temporary hardcoded database connection details
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
    
QUESTIONS = load_questions('questions')


# def load_questions(filename='questions.json'):
#     try:
#         with open(filename, 'r') as file:
#             questions = json.load(file)
#             return questions
#     except FileNotFoundError:
#         print("Error: questions.json not found.")
# QUESTIONS = load_questions('questions.json')

def get_session_list(key):
    """Retrieve a value from the session by key."""
    return session.get(key)

def set_session_list(key, value):
    """Set a value in the session for the given key."""
    session[key] = value

def init_session(category, enable_skips=False, mode='easy'):
    session.clear()
    session['categories'] = category
    session['unlocked'] = []
    session['locked'] = []
    session['lifeline_count'] = 0
    session['old_questions'] = []
    session['stage'] = 1 
    session['score'] = 0

    session['show_special_button'] = False
    session['special_used'] = False
    session['skips'] = 3 if enable_skips else 0
    session['mode'] = mode


    available_questions = [question for question in QUESTIONS if question['category'] in category]
    if available_questions:
        random_question = random.choice(available_questions)
        session['locked'] = [random_question]
        session['old_questions'] = [random_question['question_id']]
    else:
        flash("No questions available in the selected category. Please select a different category.")
        
@app.route('/', methods=['GET', 'POST'])
def index():
    """Function to render index.html and allow users to select a desired caregory of questions."""
    if request.method == 'POST':
        category_list = request.form.getlist('category')
        enable_skips = request.form.get('enable_skips') == 'yes'
        mode = request.form.get('mode', 'easy')
        if not category_list:
            flash("Please select at least one category.")
            return redirect(url_for('index'))

        available_questions = [q for q in QUESTIONS if q['category'] in category_list]
        if not available_questions:
            flash("No questions available in the selected category. Please select a different category.")
            return redirect(url_for('index'))
        init_session(category_list, enable_skips, mode)
        return redirect(url_for('game'))

    categories = sorted({question['category'] for question in QUESTIONS}, key=str.lower)
    return render_template('index.html', categories=categories)

@app.route('/game', methods=['GET', 'POST'])

def game():
    """Main route for the game logic.
        Presents player with questions one after another when player does a input.
        Handles player input: 
        Players can: 
            'place' to place a questionin relation to the timeline throug inputing a value representing a index.
            'lock' to lock their current timeline. This action decrease a lifeline. No new question can be loaded with this action.
            'quit' to return to the index.

           'score' is updated based on the number of questions placed in the timeline.
            When a question is answered through 'place' or if the timeline is locked the question is added to a list tracking what questions have already been shown
            prevening it from appering several times.
        Renders game.html template
    """
    if request.method == 'POST':
        current_id = session.get('current_id')
        next_question = get_current_question(current_id)
        timeline = sorted_timeline()
        action_buttons()

        if request.is_json:
            return jsonify({
                'score': session.get('score'),
                'lifeline_count': session.get('lifeline_count'),
                'skips': session.get('skips'),
                'locked': session.get('locked'),
                'unlocked': session.get('unlocked'),
            })
        return redirect(url_for('game'))

    next_question = next_question_available()
    if isinstance(next_question, redirect('').__class__):
        return next_question
    
    song_embed_url = song_url(next_question)  
    show_special_button = session.pop('show_special_button', False)
    timeline = sorted_timeline()
    locked = session.get('locked', [])
    unlocked = session.get('unlocked', [])
    score = session.get('score', 0)
    return render_template('game.html', show_special_button=show_special_button, next_question=next_question, song_embed_url=song_embed_url, locked=locked, unlocked=unlocked, score=score, max_index=len(timeline))
 

def check_valid_placement(combined_timeline, next_question, index):
    """
    Checks if a new next_question can be placed at the specified index in the list,
    based on the date value of the next_question and the surrounding elements in the list. It checks:

    - If the list is empty: its is considered valid.
    - If the index is 0: the next_question's date must be less than or equal to the date of the first element.
    - If the index is at the end of the list: the next_question date must be greater than or equal to the date of the last element.
    - If the index is in the middle of the list: the next_question date must be between the dates surrounding elements.

    Returns:
        Bool: True if the next_question can be validly placed at the user selected index otherwise False.

    Args:
        combined_timeline (list): A list of dictionaries, checks values at date.
        next_question (dict): The new next_question to be placed.
        index (int): The user input index  to check if the next_question can be placed at that index.
    """
    timeline = combined_timeline[:]
    timeline.insert(index, next_question)

    dates = [item['date'] for item in timeline]
    return dates == sorted(dates)

def action_quit():
    """
    Handles the quit action by clearing the session and redirecting to the index.

    returns:
        Redirect: index.html.

    Args:
        None
    """
    session.clear()
    return redirect(url_for('index'))

def action_lock():
    """
    Handles the lock action by locking the current timeline and updating the session.
    If the timeline is already locked, increase the lifeline count and check if the player has lost all lives.
    If the player has no lives left, clear the session and redirect to the index.

    returns:
        redirect: game.html or index.html.

    Args:
        None
    """
    if session.get('unlocked'):
        session['locked'] = sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])
        if len(session['unlocked']) >= 6: 
            flash(f'You have locked more than 5 at the same time you kept your lock well done you')
            session['show_special_button'] = True
 
        session['lifeline_count'] = session.get('lifeline_count', 0) + 1
        score_amount = sum((i + 1) * 100 for i in range(len(session['unlocked'])))
        session['score'] += score_amount
        session['unlocked'] = []
        lives_left = 3 - session['lifeline_count']
        flash('The timeline is locked!')
        if lives_left > 0:
            flash(f'You have {lives_left} life(s) left.')
        else:
            flash('SHOW_MODAL')
    return redirect(url_for('game'))

@app.route('/regain_lock', methods=['POST'])
def regain_lock():
    if not session.get('special_used', True):
        session['lifeline_count'] = max(session.get('lifeline_count', 0) - 1, 0)
        session['special_used'] = True
        flash('You regained a lock!')
    else:
        flash('You already used your special regain!')
    return redirect(url_for('game'))

def action_buttons():
    """
    Handles the action buttons in the game.

    Returns:
        Redirect: game.html.

    Args:
        Timeline: The current timeline of questions.
        next_question: The next question to be displayed.
        current_id: The ID of the current question.
    """
    action = request.form.get('action')
    if action == 'quit':
        return action_quit()
    elif action == 'lock':
        return action_lock()
    elif action == 'skip':
        return action_skip()
    # elif action == 'place':
    #     return action_place(timeline, next_question, current_id)
    else:
        flash('Invalid action.')
    return redirect(url_for('game'))

def action_skip():
    skips = session.get('skips', 0)
    if skips > 0:
        session['skips'] = skips - 1
        # Remove the current question from old_questions so it doesn't repeat
        current_id = session.get('current_id')
        if current_id:
            old = session.get('old_questions', [])
            old.append(current_id)
            session['old_questions'] = old
        session.pop('current_id', None)  # Force a new question to be loaded
        flash(f"Skipped! You have {session['skips']} skips left.")
    else:
        flash("No skips left!")
    return redirect(url_for('game'))

def song_url(next_question):
    """
    Extracts the song URL from the next question if the category is 'Music & Soundbites'.
    
    Return: 
        None

    Args: 
        Next_question (dict): The next question dictionary containing the category and question.
    """
    if next_question["category"] == "Music & Soundbites":
        song_url = next_question["question"]
        if "/track/" in song_url:
            try:
                track_id = song_url.split("/track/")[1].split("?")[0]
                return f"https://open.spotify.com/embed/track/{track_id}"
                # next_question["question"] = "Guess the year of this song!"
            except IndexError:
                return None  
        else:
            return None 
    return None

def next_question_available():
    """
    This function checks if there are any available questions left in the game.
    - no questions left: flash a message and redirect to index
    - if there are no current questions: select a random question from the available ones
    
    Return: 
        Next question to be displayed in the game.

    Args: 
        None
    """
    selected = session.get('categories', [])
    old_questions = session.get('old_questions', [])
    available = [question for question in QUESTIONS if question['question_id'] not in old_questions and question['category'] in selected]

    if not available:
        # flash("There's no more questions available!")
        return redirect(url_for('index'))

    if not session.get('current_id'):
        next_question = random.choice(available)
        session['current_id'] = next_question['question_id']
    else:
        next_question = next((question for question in QUESTIONS if question['question_id'] == session['current_id']), None)

    return next_question

def get_current_question(current_id):
    """
    Retrieves the current question from the session.
    
    Returns:
        dict: The current question dictionary if it exists, otherwise None.

    Args:
        current_id (str): The ID of the current question.
    """
    if current_id:
        next_question = next((question for question in QUESTIONS if question['question_id'] == current_id), None)
        return next_question
    else:
        next_question = None
    
    return  next_question

def sorted_timeline():
    """
    Returns a sorted timeline of questions based on their date.
    
    Returns:
        list: A sorted list of dictionaries containing locked and unlocked questions.

    Args:
        None
    """
    return sorted(session.get('locked', []) + session.get('unlocked', []), key=lambda e: e['date'])

@app.route('/validate_drop', methods=['POST'])
def validate_drop():
    data = request.get_json()
    question_id = data['question_id']
    timeline_ids = data['timeline']

    next_question = next((question for question in QUESTIONS if question['question_id'] == question_id), None)
    timeline = [next((question for question in QUESTIONS if question['question_id'] == qid), None) for qid in timeline_ids]
    index = timeline_ids.index(question_id)

    valid = check_valid_placement(timeline, next_question, index)


    question_text = next_question['question']
    if next_question.get('category') == 'Music & Soundbites':
        question_text = next_question.get('title', 'Spotify Track')

    history = session.get('history', [])

    if valid:
        history.append(f"Correctly placed: \"{question_text}\" at {next_question['date']}")
        session['unlocked'] = sorted(session.get('unlocked', []) + [next_question], key=lambda e: e['date'])
        
        if question_id not in session.get('old_questions', []):
            session['old_questions'] = session.get('old_questions', []) + [question_id]

        session.pop('current_id', None)

    else:
        history.append(f"Incorrect placement: \"{question_text}\" correct date is {next_question['date']}")
        score_loss = 100 * len(session['unlocked']) + 1
        session['score'] -= score_loss
        session['unlocked'] = []
        session.pop('current_id', None)
        if question_id not in session.get('old_questions', []):
            session['old_questions'] = session.get('old_questions', []) + [question_id]
        # HARD MODE: Lose a lock on incorrect placement
        if session.get('mode', 'easy') == 'hard':
            session['lifeline_count'] = session.get('lifeline_count', 0) + 1
            lives_left = 3 - session['lifeline_count']
            flash(f"You lost a lock! {lives_left} locks left.")
            if lives_left <= 0:
                flash('SHOW_MODAL')
                # Optionally, handle game over here

    session['history'] = history

    next_question = next_question_available()

    song_url_embed = song_url(next_question) if next_question else None

    return jsonify({
        'valid': valid,
        'score': session.get('score'),
        'lifeline_count': session.get('lifeline_count'),
        'skips': session.get('skips'),
        'unlocked': session.get('unlocked'),
        'locked': session.get('locked'),
        'history': session.get('history', []),
        'next_question': next_question,
        'song_embed_url': song_url_embed
    })

@app.route('/submit_score', methods=['POST'])
def submit_score():
    player_name = request.form.get('player_name')
    score = request.form.get('score', 0)
    try:
        conn = psycopg2.connect(
            dbname="aq3524",
            user="aq3524",
            password="abc123",
            host="pgserver.mau.se",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO highscores (player_name, score) VALUES (%s, %s)",
            (player_name, score)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Score submitted!")
        flash("SHOW_HIGHSCORES")  # <--- Add this line
    except Exception as e:
        flash(f"Error saving high score: {e}")
    return redirect(url_for('index'))

@app.context_processor
def inject_highscores():
    try:
        conn = psycopg2.connect(
            dbname="aq3524",
            user="aq3524",
            password="abc123",
            host="pgserver.mau.se",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, score, achieved_at FROM highscores ORDER BY score DESC, achieved_at ASC LIMIT 20")
        highscores = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        highscores = []
    return dict(highscores=highscores)

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
