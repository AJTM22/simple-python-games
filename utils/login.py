import time
# clear_screen, get_connection, display_stats, menu

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
