import random, time, psycopg, os, platform, sys
from dotenv import load_dotenv
from tabulate import tabulate
from inputimeout import inputimeout, TimeoutOccurred

def clear_screen():
    """
    Clears the screen of the terminal window

    The command depends on what is the OS of the user running the script
    """
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def get_connection():
    """
    Loads the environment variables to be used for the database

    It avoids explicitly stating who has access to the database

    Since the database used is PostgreSQL, the variables in psycopg.connect are the ones asked when logging into the PSQL terminal
    """
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
    Asks the player's name

    Query to get the player's id in the database

    If the result is None, it creates a new player in the database and queries to retrieve the player's id to be used by other functions

    Else, it welcomes the returning player and displays their stats for 10 seconds

    It then goes to the menu
    """
    clear_screen()
    with get_connection() as connection:
        with connection.cursor() as cursor:
            player_name = input('Enter your player name: ')
            query = "SELECT player_id FROM players WHERE player_name = %s;"
            cursor.execute(query, (player_name,))
            result = cursor.fetchone()

            if result is None:
                print('No record found with your player name')
                print('You must be a new player!')
                print(f'Welcome, {player_name}!')
                query = "INSERT INTO players(player_name) VALUES(%s);"
                cursor.execute(query, (player_name,))
                connection.commit()
                query = "SELECT player_id FROM players WHERE player_name = %s;"
                cursor.execute(query, (player_name,))
                result = cursor.fetchone()
                player_id = result[0]
                time.sleep(3)

            else:
                player_id = result[0]
                print(f'Welcome back, {player_name}!')
                time.sleep(3)
                clear_screen()
                display_stats(player_id)
                time.sleep(10)

    menu(player_id)

def menu(player_id):
    """
    Displays the available options of the program

    Redirects the player to the option of their choosing

    If the player enters anything outside of those options, a timeout will play and will be redirected to the menu
    """
    clear_screen()
    print('Welcome to my simple python games program!')
    print('Here are the available options:')
    print('1. Number guessing\n2. Rock paper scissor\n3. Dice roller\n4. Math quiz\n5. Even or Odd\n6. Display player stats\n7. Exit the program')
    game = input('Choose the number of the available option: ')

    match game:
        case '1':
            number_guessing(player_id, 1)
        case '2':
            rock_paper_scissor(player_id, 2)
        case '3':
            dice_roller(player_id, 3)
        case '4':
            math_quiz(player_id, 4)
        case '5':
            even_or_odd(player_id, 5)
        case '6':
            display_stats(player_id)
            time.sleep(10)
            menu(player_id)
        case '7':
            clear_screen()
            print('Thank you for playing the game!')
            time.sleep(3)
            sys.exit()
        case _:
            print('That is not an available option. Try again after a few seconds')
            time.sleep(3)
            menu(player_id)

def number_guessing(player_id, game_id: int):
    """
    Generates a random number from 1 to 100

    The player will have to guess the number to stop the loop

    Hints will be displayed to guide the player towards the number

    It tracks the number of tries the player takes to guess the number. The number of tries will be sent to the database

    If the player hasn't played the game yet, the data will be inserted into the database

    Else, the number of tries will be compared to their best score. The best score will be updated if the number of tries is lower than the best score

    Afterwards, it asks the player if they want to play again

    Any input aside from 'y' will result in returning to menu
    """
    clear_screen()
    print('Welcome to the Number Guessing Game!')
    print('Try to guess the number from 1 to 100!')
    random_number = random.randint(1, 100)
    tries = 1
    random_number_guessed = False

    while not random_number_guessed:
        guess_string = input('Enter your guess: ')

        try:
            guess = int(guess_string)
        except ValueError:
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
    
    print(f'\nYou took {tries} guesses to get the number!')
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT best_score, times_played FROM player_games WHERE player_id = %s AND game_id = %s;'
            cursor.execute(query, (player_id, game_id))
            result = cursor.fetchone()

            # If result is None, it is possible the player already exists but hasn't played any
            # Therefore, if the result is None, insert data to database
            if result is None:
                query = 'INSERT INTO player_games(player_id, game_id, best_score, latest_score, times_played) VALUES(%s, %s, %s, %s, 1);'
                cursor.execute(query, (player_id, game_id, tries, tries))

            else:
                best_score = result[0]
                times_played = result[1]

                if best_score > tries:
                    print('Congratulations! You\'ve beaten your personal best!')
                    query = 'UPDATE player_games SET best_score = %s, latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (tries, tries, times_played + 1, player_id, game_id))

                else:
                    print(f'Try to beat your personal best: {best_score} guesses!')
                    query = 'UPDATE player_games SET latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (tries, times_played + 1, player_id, game_id))
                
            connection.commit()
    
    play = input('\nDo you want to play again? (y/n): ')
    number_guessing(player_id, game_id) if play.lower() == 'y' else menu(player_id)

def rock_paper_scissor(player_id, game_id: int):
    """
    
    """
    choices = ['Rock', 'Paper', 'Scissor']
    player_move_value, computer_move_value = None, None
    player_points, computer_points = 0, 0

    i = 5
    while i > 0:
        clear_screen()
        print('Welcome to Rock-Paper-Scissor Game!')
        print('Best out of 5!')
        print('Here are your choices:')
        print('1. Rock\n2. Paper\n3. Scissor')

        player_move = input('Enter the number of your move: ')
        match player_move:
            case '1':
                player_move_value = 0
            case '2':
                player_move_value = 1
            case '3':
                player_move_value = 2
            case _:
                print('Invalid move. Try again!')
                time.sleep(2)
                continue
        
        computer_move_value = random.randint(0, 2)

        print(f'\nPlayer chose: {choices[player_move_value]}')
        print(f'Computer chose: {choices[computer_move_value]}')

        if (player_move_value - computer_move_value) % 3 == 1:
            print('Player wins a point!')
            player_points += 1
        
        elif (player_move_value - computer_move_value) % 3 == 2:
            print('Computer wins a point!')
            computer_points += 1
        
        else:
            print('It\'s a tie!')
        
        time.sleep(4)

        i -= 1
    
    clear_screen()
    print('Here are the results of the game:')
    print(f'Player\'s points: {player_points}')
    print(f'Computer points: {computer_points}')

    if player_points > computer_points:
        print('\nCongratulations! You won!')
    
    elif player_points < computer_points:
        print('\nYou lost! Better luck next time!')
        
    else:
        print('\nIt\'s a tie! Let\'s try again!')
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT best_score, times_played FROM player_games WHERE player_id = %s AND game_id = %s;'
            cursor.execute(query, (player_id, game_id))
            result = cursor.fetchone()

            if result is None:
                print(f'\n{player_points} points is your new personal best!')
                time.sleep(5)

                query = 'INSERT INTO player_games(player_id, game_id, best_score, latest_score, times_played) VALUES(%s, %s, %s, %s, 1);'
                cursor.execute(query, (player_id, game_id, player_points, player_points))
                connection.commit()

            else:
                best_score = result[0]
                times_played = result[1]
                
                if player_points > best_score:
                    print(f'\n{player_points} points is your new personal best!')
                    time.sleep(5)

                    query = 'UPDATE player_games SET best_score = %s, latest_score = %s, and times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (player_points, player_points, times_played + 1, player_id, game_id))
                    connection.commit()
                    
                else:
                    print(f'\nTry to beat your personal best: {best_score} points!')
                    time.sleep(5)

                    query = 'UPDATE player_games SET latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (player_points, times_played + 1, player_id, game_id))
                    connection.commit()

    play = input('\nDo you want to play again? (y/n): ')
    rock_paper_scissor(player_id, game_id) if play.lower() == 'y' else menu(player_id)

def dice_roller(player_id, game_id: int):
    """
    Simulates dice rolling

    The player's and computer's points will randomly chosen from 2 to 12, since the lowest value of a die is 1 and the highest value of a die is 6

    Keeps track of the player's wins and computer's wins

    Whoever has the most wins in 6 rounds, wins the game

    It then establishes a connection to the database

    Queries the best score and times played of the player

    If the result returns None, then it inserts the data into the database

    Otherwise, it compares the best score of the player to their latest score in the game

    If the latest score is greater than the best score, it updates the best score in the database alongside the latest score and times played

    Else, it only updates the latest score and times played in the database

    Lastly, it asks the player whether they want to play again

    Any input other than 'y' will return the player to the menu
    """
    clear_screen()
    print('Welcome to the Dice Roller Game!')
    print('Whoever rolls the higher value, wins the round')
    print('Whoever wins the most rounds, wins the game!')
    input('Press enter to start\n')
    player_wins, computer_wins = 0, 0

    game_round = 1
    i = 6
    while i > 0:
        print('\nDice is rolling...')
        player_points = random.randint(2, 12)
        computer_points = random.randint(2, 12)
        print(f'\nRound {game_round}')
        time.sleep(2)
        print(f'Player got {player_points}')
        time.sleep(2)
        print(f'Computer got {computer_points}')
        time.sleep(2)

        if player_points > computer_points:
            print('Player won this round!')
            player_wins += 1
        
        elif player_points < computer_points:
            print('Computer won this round!')
            computer_wins += 1
        
        else:
            print('It\'s a tie! No points were given!')
        
        time.sleep(6)
        i -= 1
        game_round += 1
    
    print(f'\nHere are the results of the game:')
    print(f'Total player wins: {player_wins}')
    print(f'Total computer wins: {computer_wins}')

    if player_wins > computer_wins:
        print('Congratulations! You won!')
    
    elif player_wins < computer_wins:
        print('Computer wins the game. Better luck next time!')
    
    else:
        print('It\'s a tie!')

    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT best_score, times_played FROM player_games WHERE player_id = %s AND game_id = %s;'
            cursor.execute(query, (player_id, game_id))
            result = cursor.fetchone()

            if result is None:
                print(f'\n{player_wins} points is your new personal best!')
                query = 'INSERT INTO player_games(player_id, game_id, best_score, latest_score, times_played) VALUES(%s, %s, %s, %s, 1);'
                cursor.execute(query, (player_id, game_id, player_wins, player_wins))
                time.sleep(3)

            else:
                best_score = result[0]
                times_played = result[1]

                if player_wins > best_score:
                    print(f'\n{player_wins} points is your new personal best!')
                    query = 'UPDATE player_games SET best_score = %s, latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (player_wins, player_wins, times_played + 1, player_id, game_id))
                    time.sleep(3)

                else:
                    print(f'\nTry to beat your personal best: {best_score} points!')
                    query = 'UPDATE player_games SET latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (player_wins, times_played + 1, player_id, game_id))
                    time.sleep(3)

            connection.commit()
    
    play = input('\nDo you want to play again? (y/n): ')
    dice_roller(player_id, game_id) if play.lower() == 'y' else menu(player_id)

def get_user_answer(sleep_timer):
    """
    Gets the player's answer with error handling

    First possible error: TimeoutOccurred
    If the sleep timer runs out before the player gets to answer, it displays a time's up message and returns None, False to be stored on the answer and game_loop variable

    Second possible error: ValueError
    Since the input of the user is converted to integer using the int function, it is to be considered that the player may mess up the answer intentionally or unintentionally
    When that happens, it displays a wrong answer message and returns None and False to the answer and game_loop variables respectively

    If no error occurs, the answer and True values will be passed to the answer and game_loop variables. The answer and game_loop variables will be further checked in the math_quiz function
    """
    try:
        answer = int(inputimeout(prompt = 'Enter your answer: ', timeout = sleep_timer))
    except TimeoutOccurred:
        print('Time\'s up!')
        time.sleep(3)
        return None, False
    except ValueError:
        print('Wrong answer!')
        time.sleep(3)
        return None, False
    
    return answer, True

def math_quiz(player_id, game_id: int):
    """
    Displays the instructions of the game and waits for the player to press enter to start

    The player will be given random numbers from 1 to 100

    The arithmetic operations are only addition, subtraction and multiplication, indicated by 1 to 3 respectively

    For comparison, the 'total' variable will hold the actual answer for comparison

    It then uses the get_user_answer function to get the user's answer and state of the game_loop variable

    There are two ways for the player to lose the game:
    - Providing the wrong answer
    - Timer runs out
    Either one of these will result in the game_loop variable becoming False. Thus, ending the game loop

    It then displays the results of the game

    It then connects to the database to insert or update the player's stats

    Lastly, it asks the user if they want to play again
    Any input other than 'y' will result in returning to the menu
    """
    clear_screen()
    print('Welcome to the Math Quiz Game!')
    print('You will enter the result on the operation of 2 numbers (e.g 1 + 1 = ?)')
    print('The range of the numbers will be 1 to 100')
    print('The arithmetic operations will be randomized!')
    print('To make things difficult, you only have a set of time to solve the problem!')
    input('\nPress enter to play\n')

    score = 0
    sleep_timer = 15
    game_loop = True
    while game_loop: # Game loop logic
        print()

        if score > 5 and sleep_timer > 3:
            sleep_timer -= 1
        
        elif score == 5:
            sleep_timer = 7

        elif score == 3:
            sleep_timer = 10

        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        operation = random.randint(1, 3)

        match operation:
            case 1: # Addition operation
                total = num1 + num2
                print(f'{num1} + {num2}')

            case 2: # Subtraction operation
                total = num1 - num2
                print(f'{num1} - {num2}')

            case 3: # Multiplication operation
                total = num1 * num2
                print(f'{num1} * {num2}')
        
        answer, game_loop = get_user_answer(sleep_timer)

        if answer == total and game_loop == True:
            score += 1
    
    clear_screen()
    print('Here are the results of the game:')
    print(f'Total score: {score} points')
    print(f'Lowest time achieved: {sleep_timer} seconds before game ends\n')

    # Database connection
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT best_score, times_played FROM player_games WHERE player_id = %s AND game_id = %s;'
            cursor.execute(query, (player_id, game_id))
            result = cursor.fetchone()

            if result is None:
                print(f'Your new personal best is {score} points!')
                query = 'INSERT INTO player_games(player_id, game_id, best_score, latest_score, times_played) VALUES(%s, %s, %s, %s, 1);'
                cursor.execute(query, (player_id, game_id, score, score))
                time.sleep(3)

            else:
                best_score = result[0]
                times_played = result[1]

                if score > best_score:
                    print(f'Congratulations! Your new personal best is {score} points!')
                    query = 'UPDATE player_games SET best_score = %s, latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (score, score, times_played + 1, player_id, game_id))
                    time.sleep(3)

                else:
                    print(f'Try to beat your personal best score: {best_score} points!')
                    query = 'UPDATE player_games SET latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (score, times_played + 1, player_id, game_id))
                    time.sleep(3)
            
            connection.commit()
    
    play = input('\nDo you want to play again? (y/n): ')
    math_quiz(player_id, game_id) if play.lower() == 'y' else menu(player_id)

def even_or_odd(player_id, game_id: int):
    """
    Function keeps track of the player's score

    There are two ways for the player to lose the game:
    - Wrong guess
    - Went above sleep_timer

    When the player makes a wrong guess, the game_loop variable will be False. Thus, ending the loop

    For added difficulty, as long as the player is progressing, the sleep timer keeps decreasing
    Once the player goes above the set sleep_timer, it will terminate the loop as well

    It will then display the results of the game

    After connecting to the database, it will try retrieve specific data from the database
    If the result is None, it will insert the data into the database
    Otherwise, compare the latest score to the player's best score to check whether to update the best_score or not
    Latest score and times played will always be changed regardless of score
    """
    clear_screen()
    print('Welcome to the Even or Odd Game!')
    print('Guess if the number is Even or Odd!')
    print('You only have a set amount of time and it decreases every time you get it correctly!')
    print('For added difficulty, type out the whole answer. Anything else ends the game!')
    input('\nPress enter to play\n')
    
    score = 0
    game_loop = True
    sleep_timer = 10
    while game_loop: # Game loop logic
        if score > 5 and sleep_timer > 2:
            sleep_timer -= 1
            random_number = random.randint(1000, 10**6)
        
        elif score == 3:
            sleep_timer = 8
            random_number = random.randint(10, 50)
        
        elif score == 5:
            sleep_timer = 5
            random_number = random.randint(50, 1000)
        
        else:
            random_number = random.randint(1, 10)

            if sleep_timer == 2:
                random_number = random.randint(1000, 10 ** 6)
        
        print()
        print(random_number)
        try:
            answer = inputimeout(prompt = 'Even or Odd: ', timeout = sleep_timer)
        except TimeoutOccurred:
            print('Times up!')
            time.sleep(2)
            game_loop = False
            continue

        if random_number % 2 == 0 and answer.lower() == 'even':
            score += 1
        
        elif random_number % 2 == 1 and answer.lower() == 'odd':
            score += 1
        
        else:
            print('Wrong answer!')
            time.sleep(3)
            game_loop = False
    
    # Display game results
    clear_screen()
    print('Here are the results of the game:')
    print(f'Total score: {score} points')
    print(f'Lowest time achieved: {sleep_timer} seconds before the game ends\n')
    
    # Database connection
    with get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT best_score, times_played FROM player_games WHERE player_id = %s AND game_id = %s;'
            cursor.execute(query, (player_id, game_id))
            result = cursor.fetchone()

            if result is None:
                print(f'Your new personal best is {score} points!')
                query = 'INSERT INTO player_games(player_id, game_id, best_score, latest_score, times_played) VALUES(%s, %s, %s, %s, 1);'
                cursor.execute(query, (player_id, game_id, score, score))
                time.sleep(3)

            else:
                best_score = result[0]
                times_played = result[1]

                if score > best_score:
                    print(f'Congratulations! Your new personal best is {score} points')
                    query = 'UPDATE player_games SET best_score = %s, latest_score = %s, times_played = %s WHERE player_id = %s AND game_id = %s;'
                    cursor.execute(query, (score, score, times_played + 1, player_id, game_id))
                    time.sleep(3)
                
                else:
                    print(f'Try to best your perosnal best: {best_score} point')
                    query = 'UPDATE player_games SET latest_score = %s, times_played = %s WHERE player_id = %s and game_id = %s;'
                    cursor.execute(query, (score, times_played + 1, player_id, game_id))
                    time.sleep(3)

            connection.commit()
    
    play = input('\nDo you want to play again> (y/n): ')
    even_or_odd(player_id, game_id) if play.lower() == 'y' else menu(player_id)

def display_stats(player_id):
    """
    The purpose is to display the player's current stats

    Establishes a connection to the database and uses a cursor to execute the query

    The query is an inner join on every table in the database

    Joins the game name, best score, latest score, and times played

    Filters it based on the player's id. The player's id is a parameter received from the login function and further passed on to other functions to track that specific player's data

    Makes use of the tabulate module for an easy display of the player's stats
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:
            print('Here are your current stats:')
            query = """
                        SELECT
                        games.game_name,
                        player_games.best_score,
                        player_games.latest_score,
                        player_games.times_played
                        
                        FROM player_games
                        
                        INNER JOIN players ON player_games.player_id = players.player_id
                        INNER JOIN games ON player_games.game_id = games.game_id
                        
                        WHERE players.player_id = %s;
                        """
            cursor.execute(query, (player_id,))
            
            headers = ['Game name', 'Best score', 'Latest score', 'Times played']
            player_data = cursor.fetchall()
            print(tabulate(player_data, headers = headers, tablefmt = 'grid'))

login() # TODO: Create a requirements.txt # TODO: Modularize the games
