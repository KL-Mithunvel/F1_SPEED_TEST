# F1_SPEED_TEST
## Autovit

<!-- Add an image of the game UI or full hardware setup here -->
<!-- Example: ![Game Overview](images/game_ui.jpg) -->

This is a real-time light reaction game built with **Tkinter GUI**, **GPIO LEDs & switches**, and a **touchscreen interface** on a Raspberry Pi 5. The player must press the correct button when a corresponding LED lights up. The game runs for 2 minutes and records scores in a local leaderboard.

---

## 🎮 Features

- 7 LEDs light up randomly — one at a time  
- Player must hit the correct switch to score  
- Game runs for exactly 2 minutes  
- Live score, timer, and GPIO debug info shown  
- Leaderboard with top 10 scores stored in a CSV  
- Emoji-enhanced GUI with full touchscreen support

---

## 🧰 Hardware Requirements

| Component           | Quantity |
|---------------------|----------|
| Raspberry Pi 4/5    | 1        |
| GPIO LEDs           | 7        |
| Push Buttons        | 7        |
| Resistors (330Ω)    | 7        |
| Touchscreen Display | Optional |
| Breadboard & Jumpers| As needed |

<!-- Add an image of your GPIO pinout or breadboard wiring here -->
<!-- Example: ![Wiring Diagram](images/wiring.png) -->

---

## 📦 Installation

1. **Clone the repository** to your Raspberry Pi:

    ```bash
    git clone https://github.com/<your-username>/<your-repo>.git
    cd <your-repo>
    ```

2. **Install required packages:**

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip fonts-noto-color-emoji git
    pip3 install RPi.GPIO
    ```

---


## 📂 Project Structure



```plaintext
.
├── main.py                   # Entry point to launch the game
├── config.py                 # Pin numbers for LEDs and switches
├── leaderboard.csv           # Stores name and score
├── gpio_test.py              # Standalone hardware test utility (in root)
├── database/
│   └── db_access.py          # CSV read/write for leaderboard
│   └── db_innit.py  
├── gui/
│   └── gui_main.py           # GUI logic with emoji support, timer, leaderboard
├── game_logic/
│   └── gpio_handler.py       # LED/button logic using RPi.GPIO
│   └── Game_loop.py 
```
## 🚀 Running the Game

Run this from the main directory:

```bash
python3 main.py
```
- Use touchscreen or keyboard to enter name and press Start Game
- LED will light up and stay on until the correct button is pressed
- Game runs for 2 minutes
- Press ESC to exit fullscreen
  
## 🧪 GPIO Pin Mapping (BOARD Mode)

| LED Index | LED Pin | Button Pin |
|-----------|---------|------------|
| 0         | 3       | 21         |
| 1         | 5       | 23         |
| 2         | 7       | 29         |
| 3         | 11      | 31         |
| 4         | 13      | 33         |
| 5         | 15      | 35         |
| 6         | 19      | 37         |

Make sure buttons pull the input HIGH when pressed (connected to 5V), and use `PUD_DOWN` in code.

---

## ✅ GPIO Testing Script

Before running the main game, test all LED/button pairs:

```bash
python3 game_logic/gpio_test.py
```
- LED lights up
- Waits for the correct button press
- Moves to next when pressed
- Use this to verify correct wiring
  
## 🏆 Leaderboard Storage

Scores are stored in:
leaderboard.csv

Format: `name,score`  
Automatically updated after each game.

---

## 📸 Screenshots & Media

<!-- Add gameplay screenshots, wiring photos, or video demo here -->
<!-- Example:
![Gameplay](images/ui.png)
![Hardware Setup](images/setup.jpg)
-->

---

## 🙌 Credits

Developed by **AUTO VIT Team**  
Special thanks to all testers and contributors 🙏
- Mithunvel KL AKA BATMAN 
- Kiran S AKA tamil one
- Kishore Priyan S AKA welding boy 
- Kiran T AKA bgl one
- Krishna R AKA ...
- Ashwin AKA robin
- Harini AKA HANI


---

## 📜 License

MIT License — Free to use, fork, and improve
