import random, time
# clear_screen, get_connection, menu
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
