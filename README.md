# ChronoLogical
ChronoLogical programming camp

# Github
https://github.com/GoblinBuilds/ChronoLogical

# To start simply run the program game_logic with terminal.
# To run frontend run app.py and click the IP adress that shows up in terminal 

# V1.0 Can now run a basic version or the game in terminal. 

# to do:

    Start with one question placed in timeline

    Score

    Menus

    Db connection

        More questions

    10 answers for win

        win screen

    Stages?

    Timelines show previous questions as cards

        Drag and drop
    
    Refaktorera koden för bättre coupling och cohesion

-------------------------------------------------------------

# to fix

    Find new problems


# Testing:
    There are test data at start och game_logic file. Just comment out the read_questions() functions you dont want to run

    You can run pytest to check valid inputs quickly(theres not alot of inputs so it wont show alot). 
        pip install pytest # install the testmodule
        python -m pytest # Run this i terminal and it will test all available inputs
        python -m pytest --html=report.html #For a html report


# Fixed

    Flask connection

    Lose unlocked answers on wrong answer

    Categories

    Lives

    Fix issue where lives decrease in the wrong order

    Add prompt for invalid input instead of showing an error message

    Ensure typing lock gives a new question as expected

    Clear saved answers when the player types quit

    Fix bug where typing exit requires entering the command twice to actually quit the game

    Reset answers properly when restarting the game after lives run out