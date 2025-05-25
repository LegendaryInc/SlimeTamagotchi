import random

def guess_number():
    print("Welcome to the Guess the Number minigame!")
    number = random.randint(1, 5)
    attempts = 3

    while attempts > 0:
        guess = input(f"Guess the number (1-5). You have {attempts} attempts left: ")
        if not guess.isdigit() or not (1 <= int(guess) <= 5):
            print("Please enter a valid number between 1 and 5.")
            continue

        guess = int(guess)
        if guess == number:
            print("Correct! You win 30 coins.")
            return 30  # Reward for winning
        else:
            attempts -= 1
            print(f"Wrong! The number was {number}. You have {attempts} attempts left.")

    print("Game over! Better luck next time.")
    return 5  # Reward for participating, even if they lose