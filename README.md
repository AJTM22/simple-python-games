****The goal is to recreate the number guessing game in the relational database course of freeCodeCamp using python****

**Games to be integrated:**
 - Number guessing game
 - Rock paper scissors
 - Dice roller
 - Math Quiz
 - Even or Odd

**Number guessing game**
 - Similar mechanics to relational database: loop until player gets the number

**Rock paper scissors**
 - Player chooses their move
 - Computer chooses a move
 - Best out of 5

**Dice roller**
 - Player vs Computer
 - Best out of 6

**Math Quiz**
 - Addition, Subtraction, Multiplication from 1 to 100
 - Fast-paced
 - One wrong answer, game ends
 - Max sleep timer is 3

**Even or Odd**
 - Fast-paced
 - One wrong answer, game ends
 - Max sleep timer is 2


****The program must connect to the postgresql database****

**Database tables**
- players table
- games table
- player_games table

**players table structure**
- player_id
- player_name

**games table**
- game_id
- game_name

**player_games table**
- player_id
- game_id
- best_score
- latest_score
- times_played
