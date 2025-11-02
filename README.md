# Simple Python Games
The goal of this project is to recreate and expand the number guessing game in the relational database course of freeCodeCamp using Python
It serves as a practice of **Python**, **PostgreSQL**, **Git**, and **Github** by integrating them into this project

---

## Project Structure
    
    games
        __init__.py
        dice_roller.py
        even_or_odd.py
        math_quiz.py
        number_guessing.py
        rock_paper_scissor.py
    
    utils
        __init__.py
        clear_screen.py
        database_connection.py
        database.py
        display_stats.py
        login.py
        menu.py
    
    .env
    README.md
    requirements.txt
    simple_python_games.py
    simple_python_games.sql

---
## Features

- 5 interactive CLI games
- Tracks user stats and scores via **PostgreSQL**
- Simple login system
- Modular structure with reusable utility scripts
- Easily extensible for new games

---
## Tech Stack
| Category | Tool |
|----------|------|
|**Language**| Python 3.13 |
|**Database**| PostgreSQL |
|**ORM / Driver**| psycopg / psycopg[binary] |
|**Version Control**| Git + Github |
|**OS**| Windows 10 |

---
## Setup Instructions

### 1.) Clone the repository
Navigate to the folder where you want to clone the repository and enter this command in the terminal:
git clone https://github.com/AJTM22/simple-python-games.git

### 2.) Install dependencies
pip install -r requirements.txt

### 3.) Configure environment variables (.env)
Create a .env file in the root directory and follow the .env.example

### 4.) Run the code
View the code for further instructions in case of not setting your own database
Otherwise, run in the terminal: python.exe simple_python_games.py
