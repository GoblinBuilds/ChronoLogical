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
        session['old_questions'] = [random_question['question_id']]
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

        return redirect(url_for('game'))

    next_question = next_question_available()
    if isinstance(next_question, redirect('').__class__):
        return next_question
    
    song_embed_url = song_url(next_question)  

    timeline = sorted_timeline()
    locked = session.get('locked', [])
    unlocked = session.get('unlocked', [])
    score = session.get('score', 0)
    return render_template('game.html', next_question=next_question, song_embed_url=song_embed_url, locked=locked, unlocked=unlocked, score=score, max_index=len(timeline))
 

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
        session['unlocked'] = []
        session['lifeline_count'] = session.get('lifeline_count', 0) + 1
        # Update score based on number of locked cards
        session['score'] = len(session['locked'])

        lives_left = 3 - session['lifeline_count']
        flash('The timeline is locked!')
        if lives_left > 0:
            flash(f'You have {lives_left} life(s) left.')
        else:
            flash('SHOW_MODAL')
    return redirect(url_for('game'))

# def action_place(timeline, next_question, current_id):
#     """
#     Handles the placement of a question in the timeline based on user input.
#     The function checks if the placement is valid and updates the session accordingly.
#     - Valid placement: add the question to the unlocked timeline and updates the old questions.
#     - Invalid placement: clear the unlocked timeline and shows an error message.
#     - Placing 5 questions: redirect to the win screen.
#     - Invalid input index: show an error message.

#     returns:
#         Redirect: game.html or win_screen.html.

#     Args:
#         Timeline: The current timeline of questions.
#         next_question: The next question to be displayed.
#         current_id: The ID of the current question.
#     """
#     user_input = request.form.get('index', -1)
#     input_index = int(user_input) if user_input.isdigit() else -1
#     if input_index == -1:
#         flash('Invalid action.')
#         return redirect(url_for('game'))
            
#     if 0 <= input_index <= len(timeline):
#         valid_placement = check_valid_placement(timeline, next_question, input_index)
#         if valid_placement:
#             session['unlocked'] = sorted(session.get('unlocked', []) + [next_question], key=lambda e: e['date'])
#             old = session.get('old_questions', [])
#             old.append(current_id)
#             session['old_questions'] = old
#             # Allow new questions to be loaded
#             session.pop('current_id', None) 
#         else:
#             session['unlocked'] = []
#             session.pop('current_id', None)
#             flash('Wrong answer, lost unlocked timeline.')

#         if len(session.get('unlocked', [])) + len(session.get('locked', [])) == 2:
#                 flash("Congratulations! You've Won!")
#                 # session.clear()
#                 return redirect(url_for('win_screen'))
#         return redirect(url_for('game'))

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
    # elif action == 'place':
    #     return action_place(timeline, next_question, current_id)
    else:
        flash('Invalid action.')
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
        flash("There's no more questions available!")
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


@app.route('/win_screen', methods=['GET', 'POST'])
def win_screen():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'submit_score':
            player_name = request.form.get('player_name')
            score = session.get('score', 0)
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
            except Exception as e:
                flash(f"Error saving high score: {e}")
            return redirect(url_for('highscores'))
        elif action == 'continue':
            old_questions = session.get('old_questions', [])
            score = session.get('score', 0)
            stage = session.get('stage', 1)

        elif action == 'restart':
            return redirect(url_for('index'))
    return render_template('win_screen.html')
#             session['unlocked'] = []
#             session['locked'] = []
#             session['lifeline_count'] = 0 

#             session['stage'] = stage + 1

#             session['old_questions'] = old_questions  
#             session['score'] = score 

#             return redirect(url_for('game')) 

#         elif action == 'restart':
#             return redirect(url_for('index'))  
    
#     return render_template('win_screen.html')

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
        session['unlocked'] = []
        session.pop('current_id', None)
        if question_id not in session.get('old_questions', []):
            session['old_questions'] = session.get('old_questions', []) + [question_id]

    session['history'] = history
    return jsonify({'valid': valid})




@app.route('/highscores')
def highscores():
    try:
        conn = psycopg2.connect(
            dbname="aq3524",
            user="aq3524",
            password="abc123",
            host="pgserver.mau.se",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, score, achieved_at FROM highscores ORDER BY score DESC, achieved_at ASC LIMIT 10")
        scores = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        flash(f"Error loading high scores: {e}")
        scores = []
    return render_template('highscores.html', scores=scores)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, use_debugger=False)
