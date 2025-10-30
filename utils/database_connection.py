from dotenv import load_dotenv
import psycopg, os

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
