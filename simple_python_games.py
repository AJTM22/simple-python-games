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

import random, time, psycopg, os, platform
from dotenv import load_dotenv

def clear_screen():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def get_connection():
    load_dotenv()

    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT"))
    )

def login():
    """
    Asks the user if they are a new player or a returning player
    If new user, create new user in the database and add all data specific to the player
    Else, enter player name and display their current records
    """
    connection = get_connection()
    cursor = connection.cursor()

    player_name = input('Enter your player name: ')
    cursor.execute("SELECT player_id FROM players WHERE player_name = %s;", (player_name,))
    player_id = cursor.fetchone()

    if player_id == None:
        print('No record found with your player name')
        print('You must be a new player!')
        print(f'Welcome, {player_name}!')
        time.sleep(3)
        connection.close()
        cursor.close()
        menu()

    else:
        print(f'Welcome back, {player_name}!')
        print('Here are your current stats:')
        print()
        time.sleep(5)
        connection.close()
        cursor.close()
        menu()

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
        case _:
            print('Game not found. Try again after a few seconds')
            time.sleep(5)
            menu()

def number_guessing():
    """
    Game will keep looping until the player gets the number
    Number of tries will be tracked and sent to the database
    Hints will be displayed to allow the user to get near the number (Higher or lower)
    
    If the player beats their personal record, a congratulatory remark will be displayed
    If not, the number of tries will be displayed
    """
    clear_screen()
    print('Welcome to the Number Guessing Game!')
    random_number = random.randint(1, 100 + 1)
    tries = 1
    random_number_guessed = False

    while not random_number_guessed:
        guess_string = input('Enter your guess: ')

        try:
            guess = int(guess_string)
        except:
            print('Invalid guess!\n')
            tries += 1
            continue

        if guess == random_number:
            random_number_guessed = True
        
        else:
            if guess < random_number:
                print('Guess higher!\n')
            
            else:
                print('Guess lower!\n')

        tries += 1
    
    # TODO: Add logic to check and store in the database
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

login()
