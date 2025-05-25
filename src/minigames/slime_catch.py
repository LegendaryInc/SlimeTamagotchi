import tkinter as tk
import random
from lang import LANGS

class SlimeCatchMinigame:
    def __init__(self, slime):
        self.slime = slime
        self.window = tk.Toplevel(slime.root)
        lang = LANGS[self.slime.language]
        self.window.title(lang["catch"])
        self.window.geometry("220x300")
        self.canvas = tk.Canvas(self.window, width=200, height=260, bg="#e0f7fa")
        self.canvas.pack(pady=10)

        self.score = 0
        self.rounds = 0
        self.max_rounds = 7
        self.speed = 120  # Initial speed in ms

        self.next_treat()

    def next_treat(self):
        self.treat_emoji = random.choice(["🍬", "🍭", "🍪", "🍎"])
        self.treat_y = 20
        self.treat_caught = False
        self.rounds += 1

        self.canvas.delete("all")
        self.treat = self.canvas.create_text(100, self.treat_y, text=self.treat_emoji, font=("Arial", 28))
        self.canvas.tag_bind(self.treat, "<Button-1>", self.catch_treat)
        self.move_treat()

    def move_treat(self):
        if self.treat_caught:
            return
        self.treat_y += 10
        self.canvas.coords(self.treat, 100, self.treat_y)
        if self.treat_y < 240:
            self.window.after(self.speed, self.move_treat)
        else:
            self.canvas.itemconfig(self.treat, text="😢")
            self.window.after(500, self.after_round)

    def catch_treat(self, event):
        if not self.treat_caught:
            self.treat_caught = True
            self.canvas.itemconfig(self.treat, text="😋")
            self.score += 1
            self.slime.coins += 5
            self.slime.happiness = min(100, self.slime.happiness + 1)
            self.slime.update_status()
            lang = LANGS[self.slime.language]
            self.canvas.create_text(100, 140, text=f"+5 {lang['coins']}!\n+1 {lang['happiness']}", font=("Arial", 12), fill="green")
            self.window.after(500, self.after_round)

    def after_round(self):
        lang = LANGS[self.slime.language]
        if self.rounds < self.max_rounds:
            self.speed = max(40, int(self.speed * 0.85))  # Speed up each round
            self.next_treat()
        else:
            bonus = self.score * 5
            happy_bonus = self.score * 2
            self.slime.coins += bonus
            self.slime.happiness = min(100, self.slime.happiness + happy_bonus)
            self.slime.update_status()
            self.canvas.delete("all")
            self.canvas.create_text(
                100, 120,
                text=f"{lang['game_over']}\n{lang['caught']}: {self.score}/{self.max_rounds}\n{lang['bonus']}: +{bonus} {lang['coins']}\n+{happy_bonus} {lang['happiness']}",
                font=("Arial", 13), fill="blue"
            )
            self.window.after(1800, self.window.destroy)