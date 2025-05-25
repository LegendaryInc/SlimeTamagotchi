# Slime Tamagotchi

A desktop virtual pet game written in Python with Tkinter.

## Features

- Feed, play, and care for your slime
- Shop for items, backgrounds, and button colors
- Inventory system with equippable items
- Minigames
- Multi-language support (English & Slovak)
- Save/load your progress

## Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/Pillow/)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Running the Game

Navigate to the `src` directory and run:

```sh
python main.py
```

## Adding Translations

To add or update translations, edit `src/lang.py`.

## Packaging for Distribution

You can use [PyInstaller](https://pyinstaller.org/) to create a standalone executable:

```sh
pip install pyinstaller
pyinstaller --onefile --add-data "us_flag.png;." --add-data "sk_flag.png;." --add-data "slime.png;." main.py
```

Make sure to include all image and data files in your distribution.

---

Enjoy your slime!