from utils.login import login
from utils.database import setup_database

if __name__ == '__main__':
    # If running the program for the first time or didn't bother creating your own database, uncomment the setup_database function to automate the creation of the database
    # setup_database()
    login()
