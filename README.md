# Fireboy and Watergirl Game

A Python implementation of the classic "Fireboy and Watergirl" game using Pygame. This project recreates the cooperative puzzle-platform game where players control two characters with different elemental properties.

## Description

Fireboy and Watergirl is a two-player cooperative game where players must work together to navigate through levels filled with puzzles and obstacles. Each character has unique properties:
- Fireboy can walk through fire but dies in water and green goo
- Watergirl can walk through water but dies in fire and green goo

Players must coordinate their movements and use their unique abilities to collect gems and reach their respective exits.

## Prerequisites

Before you begin, ensure you have Python 3.7+ installed on your system. You can check your Python version by running:
```bash
python --version
```

If you don't have venv installed, you can install it using:
```bash
# On Windows
python -m pip install --user virtualenv

# On macOS (comes pre-installed with Python3)
# No additional installation needed
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/fireboy-and-watergirl.git
cd fireboy-and-watergirl
```

2. Create a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate # Activates the virtual env

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate # Activates the virtual env
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Game

After installation, you can run the game using:
```bash
# With an activated virtual env
python main.py
```

## Controls

- Fireboy (Player 1):
  - Arrow keys for movement
  - Up arrow to jump

- Watergirl (Player 2):
  - WASD keys for movement
  - W to jump

## Contributors 
Nikola Serafimov - serafimovnikola582@gmail.com

Dushan Cimbaljevic - dushancimbalevic@gmail.com
