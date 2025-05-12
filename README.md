# ChronoLogical
ChronoLogical programming camp

# Github
https://github.com/GoblinBuilds/ChronoLogical

# To start simply run the program game_logic with terminal.
# To run frontend run app.py and click the IP adress that shows up in terminal 

# V1.0 Can now run a basic version or the game in terminal. 

# to do:


    Score - Moa

        Leaderboard

    Menus

        Pop-up window - DONE(Just need to fix some css for it) - Leonard

    Db connection - Moa

        More questions - Moa


    X answers for win 

        win screen - DONE - Leonard (win condition) and Chayatip (win screen)

    Stages (Gustav)

        1 card remains on new stage

    Timelines show previous questions as cards - Leonard and Chayatip (We made a card)


        Drag and drop - Leonard
    
    Gameover screen - Chayatip

    Lost a lifeline when lock a card - Chayatip

    Starting cards in different stages - Chayatip

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

    10 answers for win:
        Win condition (Leonard)
        win screen (Chayatip)

    Card:
         Timelines show previous questions as cards (Leonard and Chayatip)
         Animation (Chayatip)
         Start with one question (Card) placed in the timeline (Leonard)
        
    Base game logic:
        Check valid index position (Gustav)
        Sort timeline (Gustav)
        Append answers to timeline (Gustav)

    Flask connection:
        Render questions from json (Chayatip) 
        Sessions and actions (Gustav)
        Translate game logic to flask (Gustav)

    Features:

        Lose unlocked answers on wrong answer (Leonard)

        Categories (Leonard)

        Lives (Leonard)

    Bugfixes:

        Fix issue where lives decrease in the wrong order (Leonard)

        Add prompt for invalid input instead of showing an error message (Leonard)

        Ensure typing lock gives a new question as expected (Leonard)

        Clear saved answers when the player types quit (Leonard)

        Fix bug where typing exit requires entering the command twice to actually quit the game (Leonard)
        Reset answers properly when restarting the game after lives run out (Leonard)
