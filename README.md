# SDC-2-RPSLSG
# Rock-Paper-Scissors-Lizard-Spock Game

## Overview
This is a Python-based GUI game implemented using Tkinter. It is an extended version of the classic Rock-Paper-Scissors game with two additional choices: Lizard and Spock. The game offers multiple difficulty levels, score tracking, countdown timers, sound effects, and more.

## Features
- Play with 5 choices: Rock, Paper, Scissors, Lizard, and Spock
- User-selectable "Best of N" rounds
- Score tracking for user, computer, and ties
- Difficulty levels: Easy, Medium, Hard
- Visual feedback with images for choices
- Countdown timer (5 seconds) for user input each round
- Sound effects for wins, losses, and ties (optional)
- Theme switching (Light/Dark mode)
- History log of game rounds displayed in GUI
- Leaderboard saved to a local text file

## Requirements
- Python 3.x
- Tkinter (comes pre-installed with Python)
- Pillow (`pip install pillow`) — for image handling
- Optional: playsound (`pip install playsound`) for sound effects

## Setup Instructions
1. Clone or download the repository.
2. Place images named `rock.png`, `paper.png`, `scissors.png`, `lizard.png`, and `spock.png` in the project directory.
3. (Optional) Place sound files `win_sound.mp3`, `lose_sound.mp3`, and `tie_sound.mp3` in the project directory.
4. Install required packages:
    ```
    pip install pillow playsound
    ```
5. Run the game:
    ```
    python rps_game.py
    ```

## How to Play
- Enter the number of rounds to play (Best of N).
- Select difficulty level.
- Choose your move within 5 seconds per round.
- See the results and score update in real time.
- Play multiple rounds until the match finishes.
- View the leaderboard to see past game scores.

## Code Structure
- `RPSGame` class contains all game logic and UI.
- Methods handle user input, computer AI, scoring, and timer.
- Uses Tkinter for GUI, Pillow for image display.
- Threading used for asynchronous sound playback.

## Future Improvements
- Add multiplayer support.
- Use database storage for leaderboard.
- Add animations and enhanced UI.
- Improve AI with learning algorithms.

## License
This project is open source and free to use.

---

Enjoy the game and have fun!  
Feel free to contribute or report issues.
