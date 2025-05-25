import tkinter as tk
from slime import Slime

def main():
    root = tk.Tk()
    root.title("Slime Tamagotchi")
    app = Slime(root)
    root.mainloop()

if __name__ == "__main__":
    main()