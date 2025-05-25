import random

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def random_number(min_value, max_value):
    return random.randint(min_value, max_value)

def format_status(hunger, happiness, energy, coins, upgrades):
    upgrades_list = ', '.join(upgrades) if upgrades else 'None'
    return (f"Hunger: {hunger} | Happiness: {happiness} | "
            f"Energy: {energy} | Coins: {coins} | Upgrades: {upgrades_list}")