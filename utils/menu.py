import time, sys
from utils.clear_screen import clear_screen
from games.number_guessing import number_guessing
from games.rock_paper_scissor import rock_paper_scissor
from games.dice_roller import dice_roller
from games.math_quiz import math_quiz
from games.even_or_odd import even_or_odd
from utils.display_stats import display_stats
# clear_screen, number_guessing, rock_paper_scissor, dice_roller, math_quiz, even_or_odd, display_stats

def menu(player_id):
    """
    Displays the available options of the program

    Redirects the player to the option of their choosing

    If the player enters anything outside of those options, a timeout will play and will be redirected to the menu
    """
    clear_screen()
    print('Welcome to my simple python games program!')
    print('Here are the available options:')
    print('1. Number guessing\n2. Rock paper scissor\n3. Dice roller\n4. Math quiz\n5. Even or Odd\n6. Display player stats\n7. Exit the program')
    game = input('Choose the number of the available option: ')

    match game:
        case '1':
            number_guessing(player_id, 1)
        case '2':
            rock_paper_scissor(player_id, 2)
        case '3':
            dice_roller(player_id, 3)
        case '4':
            math_quiz(player_id, 4)
        case '5':
            even_or_odd(player_id, 5)
        case '6':
            display_stats(player_id)
            time.sleep(10)
            menu(player_id)
        case '7':
            clear_screen()
            print('Thank you for playing the game!')
            time.sleep(3)
            sys.exit()
        case _:
            print('That is not an available option. Try again after a few seconds')
            time.sleep(3)
            menu(player_id)
