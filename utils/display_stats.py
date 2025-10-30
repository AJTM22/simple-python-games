from tabulate import tabulate
# get_connection

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
