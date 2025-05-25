import tkinter as tk
import random
from lang import LANGS

class SlimeCleanMinigame:
    def __init__(self, slime):
        self.slime = slime
        self.window = tk.Toplevel(slime.root)
        lang = LANGS[self.slime.language]
        self.window.title(lang["clean"])
        self.window.geometry("220x300")
        self.canvas = tk.Canvas(self.window, width=200, height=260, bg="#f0f8ff")
        self.canvas.pack(pady=10)

        self.dirt_spots = []
        self.cleaned = 0
        self.max_spots = 6

        self.draw_dirt_spots()

    def draw_dirt_spots(self):
        self.canvas.delete("all")
        self.dirt_spots = []
        for _ in range(self.max_spots):
            x = random.randint(30, 170)
            y = random.randint(40, 220)
            spot = self.canvas.create_oval(x, y, x+18, y+18, fill="#8d5524", outline="")
            self.canvas.tag_bind(spot, "<Button-1>", self.clean_spot)
            self.dirt_spots.append(spot)

    def clean_spot(self, event):
        spot = self.canvas.find_withtag("current")
        if spot:
            self.canvas.delete(spot)
            self.cleaned += 1
            lang = LANGS[self.slime.language]
            self.canvas.create_text(100, 20, text=lang["cleaned"], font=("Arial", 10), fill="green")
            if self.cleaned == self.max_spots:
                self.finish_cleaning()

    def finish_cleaning(self):
        lang = LANGS[self.slime.language]
        self.slime.happiness = min(100, self.slime.happiness + 5)
        self.slime.energy = min(100, self.slime.energy + 5)
        self.slime.update_status()
        self.canvas.delete("all")
        self.canvas.create_text(
            100, 120,
            text=f"{lang['clean_done']}\n+5 {lang['happiness']}\n+5 {lang['energy']}",
            font=("Arial", 13), fill="blue"
        )
        self.window.after(1800, self.window.destroy)