import json
import os

class SaveData:
    def __init__(self, filename='slime_data.json'):
        self.filename = filename

    def save(self, slime):
        data = {
            'slime_name': slime.slime_name,
            'hunger': slime.hunger,
            'happiness': slime.happiness,
            'energy': slime.energy,
            'coins': slime.coins,
            'upgrades': slime.upgrades,
            'worn_items': slime.worn_items,
            'bg_color': slime.bg_color,
            'btn_color': slime.btn_color
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)
        print("Game saved successfully.")

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
            return data
        else:
            print("No saved game found.")
            return None

    def auto_save(self, slime):
        self.save(slime)

    def auto_load(self):
        return self.load()