import random, time
from inputimeout import inputimeout, TimeoutOccurred
from utils.clear_screen import clear_screen
from utils.database_connection import get_connection
from utils.menu import menu

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
