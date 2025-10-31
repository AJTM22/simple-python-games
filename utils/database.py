def setup_database():
    """
    Sets up the database for the new user

    It can be utilized if preferred by the user

    Imports the get_connection function from database_connection module

    Sets up a connection and cursor

    Then opens and read the simple_python_games.sql file located in the root directory

    If an error occurs, it just prints out the error
    """
    from utils.database_connection import get_connection

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                with open('../simple_python_games.sql', 'r') as file:
                    sql = file.read()
                    cursor.execute(sql)
                    connection.commit()
    
    except Exception as e:
        print(f'An error has occurred: {e}')
