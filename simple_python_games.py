# Goal is to recreate the number guessing game in the relational database course of freeCodeCamp using python

# Games to be integrated:
# - Number guessing game
# - Rock paper scissors
# - Dice roller
# - Math Quiz
# - Even or Odd

# Number guessing game
# - Similar mechanics to relational database: loop until player gets the number

# Rock paper scissors
# - Computer chooses a move
# - Player chooses their move
# - Best out of 5

# Dice roller
# - Player vs Computer
# - Best out of 6

# Math Quiz
# - Addition, Subtraction, Multiplication from 1 to 100
# - Fast-paced
# - One wrong answer, game ends

# Even or Odd
# - Fast-paced
# - One wrong answer, game ends

# The program must connect to the postgresql database

# Database structure
# players table
# games table
# player_games table

# Players table structure
# player_id
# player_name

# Games table
# game_id
# game_name

# Player-Games table
# player_id
# game_id
# best_score
# latest_score
# times_played
# date_played

import random, time, psycopg2

def menu():
    pass

def number_guessing():
    pass

def rock_paper_scissor():
    pass

def dice_roller():
    pass

def math_quiz():
    pass

def even_or_odd():
    pass