def rock_paper_scissor(player_id, game_id: int):
    """
    The player's points and computer's points will be tracked along the way

    The player's move value will change depending on their move

    The computer's move value will be chosen randomly

    Using the values given by the player and computer, it will choose the index from the choices list and display their move in text

    Given the arithmetic formula provided by ChatGPT/Copilot:
    If the resulting computation results in 1, the point goes to the player
    If the resulting computation results in 2, the point goes to the computer
    Else, the points goes to neither

    It then displays the results of the game and the corresponding remark based on the player's points

    It then connects to the database and queries the best score and times played from the database

    If the result is None, then the data is inserted into the database

    Else, the best score is compared to the player's points

    If the player's points are greater than the best score, the best score gets updated alongside the latest score, and times played

    Else, only the latest score and times played are updated in the database

    It then asks the user if they want to play again

    Any input other than 'y' will result in going back to the menu
    """
    import random, time
    from utils.clear_screen import clear_screen
    from utils.database_connection import get_connection
    from utils.menu import menu

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
