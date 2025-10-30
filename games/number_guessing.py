import random
# clear_screen, get_connection, menu
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
