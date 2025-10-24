import random, time, psycopg, os, platform, sys
from dotenv import load_dotenv
from tabulate import tabulate

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
                connection.close()
                cursor.close()
                menu(player_id)

            else:
                player_id = result[0]
                print(f'Welcome back, {player_name}!')
                display_stats(player_id)
                time.sleep(10)

    menu(player_id)

def menu(player_id):
    """
    Serves as the main menu of the program
    It displays the available games the player can play
    Depending on the choice, the player will be redirected to the game
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
            login()

def number_guessing(player_id, game_id: int):
    """
    Game will keep looping until the player gets the number
    Number of tries will be tracked and sent to the database
    Hints will be displayed to allow the user to get near the number (Higher or lower)
    
    If the player beats their personal record, a congratulatory remark will be displayed
    If not, the number of tries will be displayed
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
    Simulates a player vs computer
    Player chooses their move
    Computer choose afterwards
    Best out of 5
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
    The values are 2 - 12
    Whoever has the highest value, wins the round
    Best out of 6
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

def math_quiz(player_id, game_id: int):
    """
    
    """
    clear_screen()
    pass

def even_or_odd(player_id, game_id: int):
    """
    
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
    while game_loop:
        random_number = random.randint(1, 1000)

        if score > 5 and sleep_timer > 2:
            sleep_timer -= 1
        
        elif score == 3:
            sleep_timer = 7
        
        elif score == 5:
            sleep_timer = 5
        
        pass

def display_stats(player_id = None):
    """
    Takes in the player name or player id
    Display the stats of the player
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

login()
