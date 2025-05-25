import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os
import random
from shop import Shop
from minigames.slime_catch import SlimeCatchMinigame
from minigames.slime_clean import SlimeCleanMinigame
from save_data import SaveData
from inventory import InventoryWindow
from lang import LANGS
from tooltip import ToolTip

class Slime:
    def __init__(self, root):
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.coins = 100
        self.upgrades = []
        self.worn_items = []
        self.bg_color = "#eafaf1"
        self.btn_color = "#b6e2d3"
        self.language = "en"

        self.root = root
        self.root.title("Slime Tamagotchi")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg_color)

        # Center window on screen
        self.root.update_idletasks()
        w = 700
        h = 700
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Save/load handler
        self.save_data = SaveData()

        # --- Auto-load most recent save ---
        data = self.save_data.auto_load()
        if data:
            self.slime_name = data.get("slime_name", "Slime")
            self.hunger = data.get("hunger", 50)
            self.happiness = data.get("happiness", 50)
            self.energy = data.get("energy", 50)
            self.coins = data.get("coins", 100)
            self.upgrades = data.get("upgrades", [])
            self.worn_items = data.get("worn_items", [])
            self.bg_color = data.get("bg_color", "#eafaf1")
            self.btn_color = data.get("btn_color", "#b6e2d3")
        else:
            # Ask for slime name if no save exists
            self.slime_name = simpledialog.askstring(
                LANGS[self.language]["name_prompt"],
                LANGS[self.language]["name_prompt"],
                parent=self.root
            )
            if not self.slime_name:
                self.slime_name = "Slime"

        # Title label with slime's name
        self.title_label = tk.Label(
            root,
            text=f"{self.slime_name}",
            font=("Arial Rounded MT Bold", 28, "bold"),
            bg=self.bg_color,
            fg="#4e944f"
        )
        self.title_label.pack(pady=(18, 0))

        # Section heading for status (translated)
        self.status_heading = tk.Label(
            root,
            text=LANGS[self.language]["slime_status"],
            font=("Arial Rounded MT Bold", 16),
            bg=self.bg_color,
            fg="#4e944f"
        )
        self.status_heading.pack(pady=(10, 0))

        # Status label
        self.status_label = tk.Label(
            root,
            text=self.get_status(),
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#333"
        )
        self.status_label.pack(pady=(8, 0))

        # Frame to hold overlay and slime image together, with border
        slime_frame = tk.Frame(root, bg=self.bg_color, highlightbackground="#4e944f", highlightthickness=2, bd=0)
        slime_frame.pack(pady=(18, 0))

        # Slime image
        self.slime_canvas = tk.Canvas(root, width=160, height=180, bg=self.bg_color, highlightthickness=0)
        self.slime_canvas.pack(pady=(18, 40))

        # Draw the slime image on the canvas
        self.slime_img_path = os.path.join(os.path.dirname(__file__), "slime.png")
        self.slime_img = Image.open(self.slime_img_path).resize((140, 140))
        self.slime_photo = ImageTk.PhotoImage(self.slime_img)
        self.slime_canvas.create_image(80, 110, image=self.slime_photo)

        # --- ttk Button Style ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Rounded.TButton",
            font=("Arial", 12),
            padding=8,
            relief="flat",
            borderwidth=0,
            background=self.btn_color,
            focusthickness=3,
            focuscolor='none',
            bordercolor=self.btn_color,
            foreground="#222"
        )
        style.map("Rounded.TButton",
            background=[('active', '#7ec850'), ('!active', self.btn_color)],
            foreground=[('active', '#222'), ('!active', '#222')]
        )

        # Action buttons (grouped)
        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(pady=(0, 0))

        # Main actions row (store buttons as self attributes for language update)
        self.feed_btn = ttk.Button(btn_frame, text=LANGS[self.language]["feed"], command=self.feed, style="Rounded.TButton", width=12)
        self.feed_btn.grid(row=0, column=0, padx=10, pady=8)
        ToolTip(self.feed_btn, LANGS[self.language]["feed_tip"])

        self.play_btn = ttk.Button(btn_frame, text=LANGS[self.language]["play"], command=self.play, style="Rounded.TButton", width=12)
        self.play_btn.grid(row=0, column=1, padx=10, pady=8)
        ToolTip(self.play_btn, LANGS[self.language]["play_tip"])

        self.rest_btn = ttk.Button(btn_frame, text=LANGS[self.language]["rest"], command=self.rest, style="Rounded.TButton", width=12)
        self.rest_btn.grid(row=0, column=2, padx=10, pady=8)
        ToolTip(self.rest_btn, LANGS[self.language]["rest_tip"])

        self.status_btn = ttk.Button(btn_frame, text=LANGS[self.language]["status"], command=self.update_status, style="Rounded.TButton", width=12)
        self.status_btn.grid(row=1, column=0, padx=10, pady=8)
        ToolTip(self.status_btn, LANGS[self.language]["status_tip"])

        self.shop_btn = ttk.Button(btn_frame, text=LANGS[self.language]["shop"], command=self.open_shop, style="Rounded.TButton", width=12)
        self.shop_btn.grid(row=1, column=1, padx=10, pady=8)
        ToolTip(self.shop_btn, LANGS[self.language]["shop_tip"])

        self.catch_btn = ttk.Button(btn_frame, text=LANGS[self.language]["catch"], command=self.open_minigame, style="Rounded.TButton", width=12)
        self.catch_btn.grid(row=1, column=2, padx=10, pady=8)
        ToolTip(self.catch_btn, LANGS[self.language]["catch_tip"])

        self.clean_btn = ttk.Button(btn_frame, text=LANGS[self.language]["clean"], command=self.open_clean_minigame, style="Rounded.TButton", width=12)
        self.clean_btn.grid(row=2, column=0, padx=10, pady=8)
        ToolTip(self.clean_btn, LANGS[self.language]["clean_tip"])

        self.save_btn = ttk.Button(btn_frame, text=LANGS[self.language]["save"], command=self.save_game, style="Rounded.TButton", width=12)
        self.save_btn.grid(row=2, column=1, padx=10, pady=8)
        ToolTip(self.save_btn, LANGS[self.language]["save_tip"])

        self.load_btn = ttk.Button(btn_frame, text=LANGS[self.language]["load"], command=self.load_game, style="Rounded.TButton", width=12)
        self.load_btn.grid(row=2, column=2, padx=10, pady=8)
        ToolTip(self.load_btn, LANGS[self.language]["load_tip"])

        self.inventory_btn = ttk.Button(btn_frame, text=LANGS[self.language]["inventory"], command=self.open_inventory, style="Rounded.TButton", width=12)
        self.inventory_btn.grid(row=3, column=1, padx=10, pady=8)
        ToolTip(self.inventory_btn, LANGS[self.language]["inventory_tip"])

        # Language toggle flag buttons (both flags always visible)
        flag_frame = tk.Frame(root, bg=self.bg_color)
        flag_frame.pack(pady=(0, 0))
        us_flag = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "us_flag.png")).resize((32, 20)))
        sk_flag = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "sk_flag.png")).resize((32, 20)))
        self.flag_images = {"en": us_flag, "sk": sk_flag}
        # Show both flags, clicking one sets the language
        self.us_flag_btn = tk.Button(
            flag_frame, image=us_flag, bd=0, bg=self.bg_color, activebackground=self.bg_color,
            command=lambda: self.set_language("en")
        )
        self.us_flag_btn.pack(side="left", padx=4)
        self.sk_flag_btn = tk.Button(
            flag_frame, image=sk_flag, bd=0, bg=self.bg_color, activebackground=self.bg_color,
            command=lambda: self.set_language("sk")
        )
        self.sk_flag_btn.pack(side="left", padx=4)

        # Shop instance
        self.shop = Shop()

        self.update_status()
        self.start_stat_decay()  # Start stat decay loop

    def get_status(self):
        lang = LANGS[self.language]
        item_names = lang.get("item_names", {})
        worn = ', '.join(item_names.get(i, i) for i in self.worn_items) if self.worn_items else lang["none"]
        upgrades = ', '.join(item_names.get(i, i) for i in self.upgrades) if self.upgrades else lang["none"]
        return (f"{lang['slime_status']}\n"
                f"{lang['feed']}: {self.hunger} | {lang['play']}: {self.happiness} | "
                f"{lang['rest']}: {self.energy} | {lang['coins']}: {self.coins}\n"
                f"{lang['worn_items']}: {worn}\n"
                f"{lang['upgrades']}: {upgrades}")

    def update_status(self):
        self.status_label.config(text=self.get_status())
        self.update_overlay()
        self.update_colors()
        self.save_data.auto_save(self)

    def update_overlay(self):
        self.slime_canvas.delete("wearable")
        image_map = {}
        possible_items = {
            "Crown":   ("crown.png",   48, 32, 80, 38),
            "Hat":     ("hat.png",     54, 36, 80, 48),
            "Bow":     ("bow.png",     36, 28, 110, 135),
            "Glasses": ("glasses.png", 54, 22, 80, 120),
            "Bed":     ("bed.png",     80, 40, 80, 170),
            "Toy":     ("toy.png",     32, 32, 40, 160),
            "Lamp":    ("lamp.png",    32, 48, 140, 40),
            "Poster":  ("poster.png",  48, 48, 10, 30),
        }
        for item, (filename, w, h, x, y) in possible_items.items():
            path = os.path.join(os.path.dirname(__file__), filename)
            if os.path.exists(path):
                image_map[item] = (filename, w, h, x, y)
        if not hasattr(self, 'wearable_images'):
            self.wearable_images = {}
        for item in self.worn_items:
            if item in image_map:
                filename, w, h, x, y = image_map[item]
                path = os.path.join(os.path.dirname(__file__), filename)
                if os.path.exists(path):
                    img = Image.open(path).resize((w, h), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.wearable_images[item] = photo
                    self.slime_canvas.create_image(x, y, image=photo, tags="wearable")

    def update_colors(self):
        self.root.configure(bg=self.bg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label):
                widget.configure(bg=self.bg_color)
        style = ttk.Style()
        style.configure("TButton", background=self.btn_color)
        style.map("TButton",
                  background=[('active', '#7ec850'), ('!active', self.btn_color)])

    def feed(self):
        lang = LANGS[self.language]
        if self.coins >= 10:
            self.hunger = min(100, self.hunger + 20)
            self.coins -= 10
            messagebox.showinfo(lang["feed"], f"{lang['feed_tip']} {lang['hunger'] if 'hunger' in lang else 'Hunger'}: {self.hunger}")
        else:
            messagebox.showwarning(lang["feed"], lang["not_enough_coins"])
        self.update_status()

    def play(self):
        lang = LANGS[self.language]
        if self.energy >= 10:
            self.happiness = min(100, self.happiness + 15)
            self.energy -= 10
            messagebox.showinfo(lang["play"], f"{lang['play_tip']} {lang['happiness']}: {self.happiness}")
        else:
            messagebox.showwarning(lang["play"], lang.get("too_tired", "Your slime is too tired to play."))
        self.update_status()

    def rest(self):
        lang = LANGS[self.language]
        self.energy = min(100, self.energy + 20)
        messagebox.showinfo(lang["rest"], f"{lang['rest_tip']} {lang['energy']}: {self.energy}")
        self.update_status()

    def open_shop(self):
        self.shop.open_shop(self)

    def start_stat_decay(self):
        self.hunger = max(0, self.hunger - 2)
        self.happiness = max(0, self.happiness - 1)
        self.energy = max(0, self.energy - 1)
        self.update_status()
        self.root.after(10000, self.start_stat_decay)

    def open_minigame(self):
        SlimeCatchMinigame(self)

    def open_clean_minigame(self):
        SlimeCleanMinigame(self)

    def save_game(self):
        lang = LANGS[self.language]
        try:
            self.save_data.save(self)
            messagebox.showinfo(lang["save"], lang["game_saved"])
        except Exception as e:
            messagebox.showerror(lang["save"], f"{lang.get('save_error', 'Could not save game:')}\n{e}")

    def load_game(self):
        lang = LANGS[self.language]
        try:
            data = self.save_data.load()
            if data:
                self.slime_name = data.get("slime_name", "Slime")
                self.hunger = data.get("hunger", 50)
                self.happiness = data.get("happiness", 50)
                self.energy = data.get("energy", 50)
                self.coins = data.get("coins", 100)
                self.upgrades = data.get("upgrades", [])
                self.worn_items = data.get("worn_items", [])
                self.bg_color = data.get("bg_color", "#eafaf1")
                self.btn_color = data.get("btn_color", "#b6e2d3")
                self.update_status()
                messagebox.showinfo(lang["load"], lang["game_loaded"])
            else:
                messagebox.showwarning(lang["load"], lang["no_save"])
        except Exception as e:
            messagebox.showerror(lang["load"], f"{lang.get('load_error', 'Could not load game:')}\n{e}")

    def open_inventory(self):
        owned_items = list(set(self.worn_items) | set(self.upgrades))
        InventoryWindow(
            self.root,
            self.worn_items,
            owned_items,
            self.update_status,
            self.bg_color,
            self.btn_color,
            self.language
        )

    def toggle_language(self):
        # Deprecated: use set_language instead
        self.set_language("sk" if self.language == "en" else "en")

    def set_language(self, lang_code):
        if lang_code != self.language:
            self.language = lang_code
            self.update_language()

    def update_language(self):
        lang = LANGS[self.language]
        self.title_label.config(text=self.slime_name)
        self.status_heading.config(text=lang["slime_status"])
        self.status_label.config(text=self.get_status())
        self.feed_btn.config(text=lang["feed"])
        self.play_btn.config(text=lang["play"])
        self.rest_btn.config(text=lang["rest"])
        self.status_btn.config(text=lang["status"])
        self.shop_btn.config(text=lang["shop"])
        self.catch_btn.config(text=lang["catch"])
        self.clean_btn.config(text=lang["clean"])
        self.save_btn.config(text=lang["save"])
        self.load_btn.config(text=lang["load"])
        self.inventory_btn.config(text=lang["inventory"])
        ToolTip(self.feed_btn, lang["feed_tip"])
        ToolTip(self.play_btn, lang["play_tip"])
        ToolTip(self.rest_btn, lang["rest_tip"])
        ToolTip(self.status_btn, lang["status_tip"])
        ToolTip(self.shop_btn, lang["shop_tip"])
        ToolTip(self.catch_btn, lang["catch_tip"])
        ToolTip(self.clean_btn, lang["clean_tip"])
        ToolTip(self.save_btn, lang["save_tip"])
        ToolTip(self.load_btn, lang["load_tip"])
        ToolTip(self.inventory_btn, lang["inventory_tip"])

if __name__ == "__main__":
    root = tk.Tk()
    slime = Slime(root)
    root.mainloop()