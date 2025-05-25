import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from lang import LANGS

class InventoryWindow:
    def __init__(self, parent, worn_items, owned_items, update_callback, bg_color="#eafaf1", btn_color="#b6e2d3", language="en"):
        self.parent = parent
        self.worn_items = worn_items
        self.owned_items = owned_items
        self.update_callback = update_callback
        self.bg_color = bg_color
        self.btn_color = btn_color
        self.language = language
        lang = LANGS[self.language]
        item_names = lang.get("item_names", {})

        self.win = tk.Toplevel(self.parent)
        self.win.title(lang["inventory"])
        self.win.configure(bg=self.bg_color)
        tk.Label(self.win, text=lang["inventory"], font=("Arial Rounded MT Bold", 16), bg=self.bg_color).pack(pady=8)

        # Group items by type/slot, include all shop items
        slots = {
            lang.get("Head", "Head"): ["Crown", "Hat", "Party Hat"],
            lang.get("Face", "Face"): ["Glasses", "Mustache"],
            lang.get("Body", "Body"): ["Bow", "Scarf", "Flower", "Heart"],
            lang.get("Room", "Room"): ["Bed", "Toy", "Lamp", "Poster", "Star"],
            lang.get("Background", "Background"): [
                "Pink Background", "Blue Background", "Mint Background", "Yellow Background", "Purple Background", "Gray Background"
            ],
            lang.get("Buttons", "Buttons"): [
                "Green Buttons", "Pink Buttons", "Blue Buttons", "Yellow Buttons", "Purple Buttons", "Gray Buttons"
            ]
        }

        for slot, items in slots.items():
            frame = tk.LabelFrame(self.win, text=slot, bg=self.bg_color, font=("Arial", 12, "bold"), fg="#4e944f")
            frame.pack(padx=10, pady=6, fill="x")
            for item in items:
                if item in self.owned_items:
                    img_path = os.path.join(os.path.dirname(__file__), f"{item.lower().replace(' ', '_')}.png")
                    if os.path.exists(img_path):
                        img = Image.open(img_path).resize((32, 24))
                        photo = ImageTk.PhotoImage(img)
                    else:
                        photo = None
                    is_equipped = item in self.worn_items
                    # Use translated item name
                    display_name = item_names.get(item, item)
                    btn_text = f"{lang['inventory_unequip'] if is_equipped else lang['inventory_equip']} {display_name}"
                    btn = ttk.Button(frame, text=btn_text, style="Rounded.TButton",
                                     command=lambda i=item: self.toggle_equip(i), width=18)
                    btn.pack(side="left", padx=6, pady=4)
                    if photo:
                        lbl = tk.Label(frame, image=photo, bg=self.bg_color)
                        lbl.image = photo
                        lbl.pack(side="left", padx=2)

    def toggle_equip(self, item):
        # Only one per slot
        slot_map = {
            "Crown": "Head", "Hat": "Head", "Party Hat": "Head",
            "Glasses": "Face", "Mustache": "Face",
            "Bow": "Body", "Scarf": "Body", "Flower": "Body", "Heart": "Body",
            "Bed": "Room", "Toy": "Room", "Lamp": "Room", "Poster": "Room", "Star": "Room"
        }
        slot = slot_map.get(item)
        if slot:
            for i in list(self.worn_items):
                if slot_map.get(i) == slot:
                    self.worn_items.remove(i)
        if item not in self.worn_items:
            self.worn_items.append(item)
        self.update_callback()
        self.win.destroy()
        # Re-open to refresh
        InventoryWindow(self.parent, self.worn_items, self.owned_items, self.update_callback, self.bg_color, self.btn_color, self.language)