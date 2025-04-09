from random import randint
timeline_list = []

def main():
    generate_a_start_timeline()
    print_timeline()
    get_user_answer()
    print_timeline()

def generate_a_start_timeline():
    """
    The Function generate a random starting year from 1-2025 and
    append the starting year into the list: timeline_list

    return:
    int: the starting year in the timelines
    """
    starting_year = randint(1,2025)
    timeline_list.append(starting_year)
    return starting_year

def get_user_answer():
    """
    This version of the function asks the user to input a year and
    append the input into the list: timeline_list
    
    return:
    int: the year that the user put in
    """
    print("Year:")
    user_timeline = int(input())
    timeline_list.append(user_timeline)
    return user_timeline

def print_timeline():
    """Funktionen sorterar årtalen i listan och skriver ut det."""
    timeline_list.sort()
    print(timeline_list)

main()