import json
import random

def main():
    """
    This is the main function that runs the program and display the menu.
    It allows the user to choose between displaying a question or exiting the program.

        args:
            None
        returns:
            None
    """
    while True:
        print("*"*15)
        print("1. Display a question")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_question()
        elif choice == "2":
            break
        else:
            print("Invalid choice, please try again.")
            main()

def read_question():
    """
    This function reads a JSON file and returns the data as a list.
    If the file is not found, print an error message.

        args:
            None
        returns:
            A list of questions from the JSON file or an empty list if the file is not found.
    """
    try:
        with open ('questions.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        

def display_question():
    """
    This function selects a random question from the function read_question, which returns data, and then prints it.

        args:
            None
        returns:
            None
    """
    data = read_question()
    if data:
        random_question = random.choice(data) 
        print(random_question['question'])
    else:
        print("No questions available.")
    
main()