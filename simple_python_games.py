# Goal is to recreate the number guessing game in the relational database course of freeCodeCamp using python

# Games to be integrated:
# - Number guessing game
# - Rock paper scissors
# - Dice roller
# - Math Quiz
# - Even or Odd

# Number guessing game
# - Similar mechanics to relational database: loop until player gets the number

# Rock paper scissors
# - Computer chooses a move
# - Player chooses their move
# - Best out of 5

# Dice roller
# - Player vs Computer
# - Best out of 6

# Math Quiz
# - Addition, Subtraction, Multiplication from 1 to 100
# - Fast-paced
# - One wrong answer, game ends

# Even or Odd
# - Fast-paced
# - One wrong answer, game ends

# The program must connect to the postgresql database

# Database structure
# players table
# games table
# player_games table

# Players table structure
# player_id
# player_name

# Games table
# game_id
# game_name

# Player-Games table
# player_id
# game_id
# best_score
# latest_score
# times_played

import random, time, psycopg2, os, platform

def clear_screen():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def login():
    """
    Asks the user if they are a new player or a returning player
    If new user, create new user in the database and add all data specific to the player
    Else, enter player name and display their current records
    """
    pass

def menu():
    """
    Serves as the main menu of the program
    It displays the available games the player can play
    Depending on the choice, the player will be redirected to the game
    """
    clear_screen()
    print('Welcome to my simple python games program!')
    print('Here are the available games:')
    print('1. Number guessing\n2. Rock paper scissor\n3. Dice roller\n4. Math quiz\n5. Even or Odd')
    game = input('Choose the number of the game you want to play: ')

    match game:
        case '1':
            number_guessing()
        case '2':
            rock_paper_scissor()
        case '3':
            dice_roller()
        case '4':
            math_quiz()
        case '5':
            even_or_odd()

def number_guessing():
    """
    
    """
    clear_screen()
    pass

def rock_paper_scissor():
    """
    
    """
    clear_screen()
    pass

def dice_roller():
    """
    
    """
    clear_screen()
    pass

def math_quiz():
    """
    
    """
    clear_screen()
    pass

def even_or_odd():
    """
    
    """
    clear_screen()
    pass

