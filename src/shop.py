import tkinter as tk
from tkinter import messagebox, simpledialog
from lang import LANGS

class Shop:
    def __init__(self):
        self.upgrades = {
            "Hat": {"price": 50, "type": "worn"},
            "Bow": {"price": 60, "type": "worn"},
            "Glasses": {"price": 80, "type": "worn"},
            "Crown": {"price": 120, "type": "worn"},
            "Toy": {"price": 75, "type": "item"},
            "Bed": {"price": 100, "type": "item"},
            "Lamp": {"price": 90, "type": "item"},
            "Poster": {"price": 40, "type": "item"},
            # Background color options
            "Pink Background": {"price": 100, "type": "bg_color", "color": "#ffe0f7"},
            "Blue Background": {"price": 100, "type": "bg_color", "color": "#e0f0ff"},
            "Mint Background": {"price": 100, "type": "bg_color", "color": "#eafaf1"},
            "Yellow Background": {"price": 100, "type": "bg_color", "color": "#fff9e0"},
            "Purple Background": {"price": 120, "type": "bg_color", "color": "#f3e0ff"},
            "Gray Background": {"price": 80, "type": "bg_color", "color": "#f0f0f0"},
            # Button color options
            "Green Buttons": {"price": 80, "type": "btn_color", "color": "#b6e2d3"},
            "Pink Buttons": {"price": 80, "type": "btn_color", "color": "#ffb6d5"},
            "Blue Buttons": {"price": 80, "type": "btn_color", "color": "#b6d6ff"},
            "Yellow Buttons": {"price": 80, "type": "btn_color", "color": "#ffe9b6"},
            "Purple Buttons": {"price": 100, "type": "btn_color", "color": "#dab6ff"},
            "Gray Buttons": {"price": 60, "type": "btn_color", "color": "#e0e0e0"},
            "Rename Slime": {"price": 30, "type": "rename"},
        }

    def open_shop(self, slime):
        lang = LANGS[slime.language]
        shop_win = tk.Toplevel()
        shop_win.title(lang["shop"])
        tk.Label(shop_win, text=lang["shop_tip"], font=("Arial", 12, "bold")).pack(pady=5)

        for name, info in self.upgrades.items():
            def make_cmd(item=name):
                return lambda: self.buy_upgrade(slime, item, shop_win)
            # Use translated item name if available
            display_name = lang.get("item_names", {}).get(name, name)
            btn = tk.Button(
                shop_win,
                text=f"{display_name}: {info['price']} {lang['coins']}",
                width=32,
                command=make_cmd()
            )
            btn.pack(pady=2)

    def buy_upgrade(self, slime, choice, win):
        lang = LANGS[slime.language]
        info = self.upgrades[choice]
        display_name = lang.get("item_names", {}).get(choice, choice)
        if info["type"] == "worn" and choice in slime.worn_items:
            messagebox.showinfo(lang["shop"], f"{lang['already_own']} {display_name}.")
            return
        if info["type"] == "item" and choice in slime.upgrades:
            messagebox.showinfo(lang["shop"], f"{lang['already_own']} {display_name}.")
            return
        if slime.coins >= info["price"]:
            slime.coins -= info["price"]
            if info["type"] == "worn":
                slime.worn_items.append(choice)
            elif info["type"] == "item":
                slime.upgrades.append(choice)
            elif info["type"] == "bg_color":
                slime.bg_color = info["color"]
            elif info["type"] == "btn_color":
                slime.btn_color = info["color"]
            elif info["type"] == "rename":
                new_name = simpledialog.askstring(lang["shop"], lang["name_prompt"], parent=win)
                if new_name:
                    slime.slime_name = new_name
                    if hasattr(slime, "title_label"):
                        slime.title_label.config(text=new_name)
            slime.update_status()
            messagebox.showinfo(lang["shop"], f"{lang['bought']} {display_name}!")
        else:
            messagebox.showwarning(lang["shop"], lang["not_enough_coins"])