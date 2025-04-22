import json
import random


#######################################################
"""Test modules!"""
# def read_question(): #Test Regular values
#     return [
#         {"ID": 1, "date": 0, "question": "When was year 0?", "category": "History"},
#         {"ID": 2, "date": 1000, "question": "When was year 1000?", "category": "History"},
#         {"ID": 3, "date": 2000, "question": "When was year 2000?", "category": "History"},
#         {"ID": 4, "date": 3000, "question": "When was year 3000?", "category": "Sport"},
#     ]

# def read_question(): #Test Negative values
#     return [
#         {"ID": 1, "date": -1, "question": "When was year -1?", "category": "History"},
#         {"ID": 2, "date": -1000, "question": "When was year -1000?", "category": "History"},
#         {"ID": 3, "date": 2000, "question": "When was year 2000?", "category": "History"},
#         {"ID": 4, "date": 0, "question": "When was year 0?", "category": "History"},
#     ]

# def read_question(): #Test big numbers, and same numbers
#     return [
#         {"ID": 1, "date": -999999999999999, "question": "When was year -999999999999999?", "category": "History"},
#         {"ID": 2, "date": 999999999999999, "question": "When was year 999999999999999?", "category": "History"},
#         {"ID": 3, "date": 2000, "question": "When was year 2000?", "category": "History"},
#         {"ID": 4, "date": 2000, "question": "When was year 2000 again?", "category": "History"},
#         {"ID": 4, "date": 2000, "question": "When was year 2000 again again?", "category": "History"},
#         {"ID": 5, "date": 0, "question": "When was year 0?", "category": "History"},
#         {"ID": 6, "date": 0, "question": "When was year 0?", "category": "History"},
#     ]
"""End of Test modules!"""
######################################################

def read_question():
    """
    This function reads a JSON file and returns the data as a list.
    If the file is not found, print an error message.
        Args:
            None
        Returns:
            A list of questions from the JSON file.
    """

    try:
        with open ('questions.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")


#Global variables to store lists.
UNLOCKED_LIST = []
LOCKED_LIST = []

def get_combined_timeline_list():
    """
    Combines LOCKED_LIST and UNLOCKED_LIST into a single list,
    sorts the combined list by the 'date' value, and returns the sorted timeline.

    Returns:
        list: A sorted list containing elements from both LOCKED_LIST and UNLOCKED_LIST, ordered by date.
    """

    combined_timeline = []
    for previous_lists in LOCKED_LIST:
        combined_timeline.extend(previous_lists)
    combined_timeline.extend(UNLOCKED_LIST)

    return sorted(combined_timeline, key=lambda e: e["date"])

def check_valid_placement(combined_timeline, entry, index):
    """
    Checks if a new entry can be placed at the specified index in the list,
    based on the date value of the entry and the surrounding elements in the list. It checks:

    - If the list is empty: its is considered valid.
    - If the index is 0: the entry's date must be less than or equal to the date of the first element.
    - If the index is at the end of the list: the entry date must be greater than or equal to the date of the last element.
    - If the index is in the middle of the list: the entry date must be between the dates surrounding elements.

    Args:
        combined_timeline (list): A list of dictionaries, checks values at date.
        entry (dict): The new entry to be placed.
        index (int): The user input index  to check if the entry can be placed at that index.

    Returns:
        bool: True if the entry can be validly placed at the user selected index otherwise False.
    """

    date = entry["date"]
    if not combined_timeline:
        return True
    if index == 0:
        return date <= combined_timeline[0]["date"]
    elif index == len(combined_timeline):
        return date >= combined_timeline[-1]["date"]
    else:
        return combined_timeline[index - 1]["date"] <= date <= combined_timeline[index]["date"]

def print_question(current_entry):
        print(f"\n Question: {current_entry['question']}")
        # print(f" date to place: {current_entry['date']}")

def get_available_questions(all_questions, old_questions, category=None):
    """
    Filters the list of all questions to return only those that haven't been used.
    
    Args:
        all_questions (list): List of all available questions.
        old_questions: IDs of questions already used.
        category (str): Filter by category, if needed, manual input needed.
    Returns:
        list: A list of available questions.
    """

    filtered_questions = [entry for entry in all_questions if entry["ID"] not in old_questions]
    
    if category:
        filtered_questions = [entry for entry in filtered_questions if entry.get("category", "").lower() == category.lower()]
    
    return filtered_questions



def display_question_and_timeline(current_entry, combined_timeline):
    """
    Displays the current question and the combined timeline.
    
    Args:
        current_entry (dict): The current question entry to be displayed.
        combined_timeline (list): The current combined timeline to be displayed.
    
    Returns:
        None
    """

    print_question(current_entry)
    print(f"\nTimeline: {[entry['date'] for entry in combined_timeline]}")

def get_user_input(combined_timeline):
    """
    Prompts the user for input with basic validation.
    
    Args:
        combined_timeline (list): The current combined timeline
    
    Returns:
        str: The user's input: either index, lock, or quit
    """

    return input(f"Choose a position, from index 0 to {len(combined_timeline)} to place the date (For example if you want to place it in 1st position write 0). Write: 'lock' to lock the timeline, or 'quit' to quit: ").strip().lower()

def lock_unlocked_list():
    """
    Handles the locking of the timeline if there are lockable objects.
    
    Returns:
        bool: True if the timeline was locked or returns False.
    """

    if UNLOCKED_LIST:
        LOCKED_LIST.append(UNLOCKED_LIST.copy())
        UNLOCKED_LIST.clear()
        print("Timeline locked!")
        return True
    else:
        print("There's nothing to lock.")
        return False

def handle_user_input(user_input, combined_timeline, current_entry):
    """
    Handles the user input and performs the appropriate action.
    
    Args:
        user_input (str): The user input.
        combined_timeline (list): The current combined timeline.
        current_entry (dict): The current question entry.
    
    Returns:
        bool: True if the game should continue, False if it should end.
    """

    if user_input == 'quit':
        print("bay bay")
        return False
    elif user_input == 'lock':
        return lock_unlocked_list()
    elif user_input.isdigit():
        index = int(user_input)
        if 0 <= index <= len(combined_timeline):
            if check_valid_placement(combined_timeline, current_entry, index):
                UNLOCKED_LIST.append(current_entry)
                print("Correct placement!")
            else:
                lifeline()
        else:
            print("Please enter a number between 0 and the length of the timeline.")
    else:
        print("Please enter a valid index, lock, or quit.")
    
    return True


def lifeline():
    """
    This function handles the life of the player and end the game if the player has no lives left.
    
    Args:
        None

    Returns:
        None
    """
    if not hasattr(lifeline, "count"):
        lifeline.count = 0

    if lifeline.count < 2:
        print("The date doesn't fit at that position.")
        lifeline.count += 1
        print(f"You have 3/{3 - lifeline.count} lives left.")
    else:
        print("\nYou have no lives left. Game Over.")
        print("Going back to menu.")
        main()

lifeline.count = 0
    
def game_logic():
    """
    Runs the main game loop
    """

    old_questions = set()
    all_questions = read_question()  

    while True:
        available = get_available_questions(all_questions, old_questions)
        
        if not available:
            print("\nThere're no questions left. And you win I guess?")
            break

        current_entry = random.choice(available)
        old_questions.add(current_entry["ID"])

        combined_timeline = get_combined_timeline_list()
        display_question_and_timeline(current_entry, combined_timeline)

        user_input = get_user_input(combined_timeline)
        
        if not handle_user_input(user_input, combined_timeline, current_entry):
            break


def game_logic_with_categories():
    """
    Runs the main game loop for categories.
    Allows different categories to be selected.
    """
    old_questions = set()
    all_questions = read_question()  

    while True:

        available = get_available_questions(all_questions, old_questions, category=None)
        duplicate = set()
        print("\nAvailable categories:")
        for entry in available:
            if entry["category"] not in duplicate:
                print(entry["category"])
                duplicate.add(entry["category"])
        category = input("Choose a category(or write 'quit' to return to menu): ").lower()
        if category == "sport":
            available = get_available_questions(all_questions, old_questions, category="Sport")
            game_logic_for_categories(available, old_questions)

        elif category == "history":
            available = get_available_questions(all_questions, old_questions, category="History")
            game_logic_for_categories(available, old_questions)

        elif category == "quit":
            print("bay bay")
            return main()


def game_logic_for_categories(available, old_questions):

    """
    Runs the main game loop for categories.
    """

    while True:   
        if not available:
            print("\nThere're no questions left.")
            break

        current_entry = random.choice(available)
        old_questions.add(current_entry["ID"])

        combined_timeline = get_combined_timeline_list()
        display_question_and_timeline(current_entry, combined_timeline)

        user_input = get_user_input(combined_timeline)
        
        if not handle_user_input(user_input, combined_timeline, current_entry):
            break

def main():
    """
    This is the main function that runs the program and display the menu.
    """

    while True:
        print("*"*15)
        print("1. Display a question")
        print("2. Choose a category")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            game_logic()
        elif choice == "2":
            game_logic_with_categories()
        elif choice == "3":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
