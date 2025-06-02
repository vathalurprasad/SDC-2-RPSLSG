import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import threading
import os

try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Lizard Spock")

        # Choices and rules
        self.choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
        self.wins = {
            'rock': ['scissors', 'lizard'],
            'paper': ['rock', 'spock'],
            'scissors': ['paper', 'lizard'],
            'lizard': ['paper', 'spock'],
            'spock': ['rock', 'scissors']
        }

        # Scores and rounds
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0
        self.max_rounds = 5
        self.last_user_choice = None
        self.timer_thread = None
        self.time_left = 0
        self.timer_running = False

        # Setup UI
        self.setup_ui()
        self.load_images()
        self.change_theme('light')

    def setup_ui(self):
        # Round input
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="Best of rounds:").grid(row=0, column=0)
        self.rounds_entry = tk.Entry(frame_top, width=5)
        self.rounds_entry.insert(0, "5")
        self.rounds_entry.grid(row=0, column=1)

        # Difficulty level
        tk.Label(frame_top, text="Difficulty:").grid(row=0, column=2, padx=(10,0))
        self.difficulty = tk.StringVar(value='Easy')
        diff_menu = tk.OptionMenu(frame_top, self.difficulty, 'Easy', 'Medium', 'Hard')
        diff_menu.grid(row=0, column=3)

        # Theme switch
        tk.Label(frame_top, text="Theme:").grid(row=0, column=4, padx=(10,0))
        self.theme = tk.StringVar(value='light')
        theme_menu = tk.OptionMenu(frame_top, self.theme, 'light', 'dark', command=self.change_theme)
        theme_menu.grid(row=0, column=5)

        # Start button
        self.start_btn = tk.Button(frame_top, text="Start Game", command=self.start_game)
        self.start_btn.grid(row=0, column=6, padx=10)

        # Scores display
        self.score_label = tk.Label(self.root, text="User: 0  Computer: 0  Ties: 0", font=("Arial", 12))
        self.score_label.pack(pady=5)

        # Timer label
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.timer_label.pack()

        # Images display
        frame_imgs = tk.Frame(self.root)
        frame_imgs.pack(pady=5)

        self.user_img_label = tk.Label(frame_imgs)
        self.user_img_label.grid(row=0, column=0, padx=20)
        tk.Label(frame_imgs, text="You").grid(row=1, column=0)

        self.computer_img_label = tk.Label(frame_imgs)
        self.computer_img_label.grid(row=0, column=1, padx=20)
        tk.Label(frame_imgs, text="Computer").grid(row=1, column=1)

        # Buttons for choices
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)
        self.choice_buttons = {}
        for choice in self.choices:
            btn = tk.Button(frame_buttons, text=choice.title(), command=lambda c=choice: self.player_choice(c), width=10)
            btn.pack(side=tk.LEFT, padx=5)
            self.choice_buttons[choice] = btn

        # History log
        self.history_text = tk.Text(self.root, height=10, width=60, state=tk.DISABLED)
        self.history_text.pack(pady=10)

        # Leaderboard button
        self.leaderboard_btn = tk.Button(self.root, text="Show Leaderboard", command=self.show_leaderboard)
        self.leaderboard_btn.pack(pady=(0,10))

        # Disable buttons until game starts
        self.disable_choice_buttons()

    def load_images(self):
        self.img_map = {}
        for choice in self.choices:
            path = f"{choice}.png"
            if os.path.exists(path):
                img = Image.open(path).resize((60, 60))
                self.img_map[choice] = ImageTk.PhotoImage(img)
            else:
                # Placeholder with text if no image file
                self.img_map[choice] = None

    def start_game(self):
        # Validate rounds input
        try:
            rounds = int(self.rounds_entry.get())
            if rounds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for rounds.")
            return

        self.max_rounds = rounds
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0
        self.last_user_choice = None
        self.update_score_label()
        self.clear_history()
        self.enable_choice_buttons()
        self.update_images(None, None)
        self.start_timer()

    def player_choice(self, choice):
        if self.timer_running:
            self.timer_running = False  # stop timer early because user chose
        self.play_round(choice)

    def play_round(self, user_choice):
        computer_choice = self.get_computer_choice()
        self.last_user_choice = user_choice

        self.update_images(user_choice, computer_choice)

        result = self.decide_winner(user_choice, computer_choice)
        self.rounds_played += 1

        self.update_score_label()
        self.append_history(f"Round {self.rounds_played}: You - {user_choice.title()} | Computer - {computer_choice.title()} | {result}")

        if self.rounds_played >= self.max_rounds:
            self.end_game()
        else:
            self.start_timer()

    def get_computer_choice(self):
        diff = self.difficulty.get()
        if diff == 'Easy':
            return random.choice(self.choices)
        elif diff == 'Medium':
            # Try to beat user's last move by choosing winning move
            if self.last_user_choice:
                counters = [c for c, beats in self.wins.items() if self.last_user_choice in beats]
                if counters:
                    return random.choice(counters)
            return random.choice(self.choices)
        else:  # Hard: weight choices more likely to win
            weights = []
            for c in self.choices:
                if self.last_user_choice and self.last_user_choice in self.wins[c]:
                    weights.append(0.4)  # Strong chance to counter
                else:
                    weights.append(0.12)
            return random.choices(self.choices, weights=weights, k=1)[0]

    def decide_winner(self, user, computer):
        if user == computer:
            self.ties += 1
            self.play_sound('tie')
            return "It's a tie!"
        elif computer in self.wins[user]:
            self.user_score += 1
            self.play_sound('win')
            return "You win!"
        else:
            self.computer_score += 1
            self.play_sound('lose')
            return "You lose!"

    def update_score_label(self):
        self.score_label.config(text=f"User: {self.user_score}  Computer: {self.computer_score}  Ties: {self.ties}")

    def update_images(self, user_choice, computer_choice):
        if user_choice and self.img_map.get(user_choice):
            self.user_img_label.config(image=self.img_map[user_choice])
        else:
            self.user_img_label.config(image='')

        if computer_choice and self.img_map.get(computer_choice):
            self.computer_img_label.config(image=self.img_map[computer_choice])
        else:
            self.computer_img_label.config(image='')

    def append_history(self, text):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def clear_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete('1.0', tk.END)
        self.history_text.config(state=tk.DISABLED)

    def disable_choice_buttons(self):
        for btn in self.choice_buttons.values():
            btn.config(state=tk.DISABLED)

    def enable_choice_buttons(self):
        for btn in self.choice_buttons.values():
            btn.config(state=tk.NORMAL)

    def play_sound(self, result_type):
        if not SOUND_AVAILABLE:
            return
        sounds = {
            'win': 'win_sound.mp3',
            'lose': 'lose_sound.mp3',
            'tie': 'tie_sound.mp3'
        }
        file = sounds.get(result_type)
        if file and os.path.exists(file):
            threading.Thread(target=playsound, args=(file,), daemon=True).start()

    def start_timer(self):
        self.time_left = 5
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            self.timer_label.config(text="")
            return
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up! Auto-selecting...")
            self.timer_running = False
            self.play_round(random.choice(self.choices))

    def end_game(self):
        self.disable_choice_buttons()
        winner = "It's a tie!"
        if self.user_score > self.computer_score:
            winner = "You won the game!"
        elif self.user_score < self.computer_score:
            winner = "Computer won the game!"
        messagebox.showinfo("Game Over", winner)
        self.timer_label.config(text="")
        self.save_scores()

    def save_scores(self):
        try:
            with open('leaderboard.txt', 'a') as f:
                f.write(f"User: {self.user_score} | Computer: {self.computer_score} | Ties: {self.ties}\n")
        except Exception as e:
            print("Error saving scores:", e)

    def show_leaderboard(self):
        try:
            with open('leaderboard.txt', 'r') as f:
                scores = f.read()
        except FileNotFoundError:
            scores = "No scores yet."
        messagebox.showinfo("Leaderboard", scores)

    def change_theme(self, theme=None):
        # Allow theme to be passed by OptionMenu callback or direct call
        if theme:
            self.theme.set(theme)
        theme = self.theme.get()

        if theme == 'dark':
            bg = '#222222'
            fg = '#f0f0f0'
            btn_bg = '#555555'
        else:
            bg = '#f0f0f0'
            fg = '#000000'
            btn_bg = '#e0e0e0'

        self.root.config(bg=bg)
        for widget in self.root.winfo_children():
            self._set_widget_colors(widget, bg, fg, btn_bg)

    def _set_widget_colors(self, widget, bg, fg, btn_bg):
        # Recursively set colors for widget and children
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass
        if isinstance(widget, tk.Button):
            try:
                widget.config(bg=btn_bg)
            except:
                pass
        for child in widget.winfo_children():
            self._set_widget_colors(child, bg, fg, btn_bg)


if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()
