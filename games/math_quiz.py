from inputimeout import inputimeout, TimeoutOccurred
import time, random
# clear_screen, get_connection, menu

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
