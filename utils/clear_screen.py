import os, platform

def clear_screen():
    """
    Clears the screen of the terminal window

    The command depends on what is the OS of the user running the script
    """
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)
