import tkinter as tk
from threading import Thread
import random
import time

from database.db_access import insert_score, fetch_top_scores
from config import TIMER_DURATION

def launch_gui():
    root = tk.Tk()
    root.title("F1 Game!")

    # Player Name Entry
    name_label = tk.Label(root, text="Enter Name:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Timer
    timer_label = tk.Label(root, text="Time: 00:00.000")
    timer_label.pack()

    # Start Button
    def start_game():
        player_name = name_entry.get().strip()
        if not player_name:
            return  # Reject empty names

        def run_game():
            start_time = time.time()
            while time.time() - start_time < TIMER_DURATION:
                elapsed = time.time() - start_time
                mins = int(elapsed // 60)
                secs = int(elapsed % 60)
                ms = int((elapsed % 1) * 1000)
                timer_label.config(text=f"Time: {mins:02d}:{secs:02d}.{ms:03d}")
                time.sleep(0.05)
            score = random.randint(10, 100)
            insert_score(player_name, score)
            update_leaderboard()

        Thread(target=run_game, daemon=True).start()

    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.pack()

    # Leaderboard
    leaderboard_frame = tk.Frame(root)
    leaderboard_frame.pack()

    leaderboard_list = tk.Listbox(leaderboard_frame, width=40)
    leaderboard_list.pack()

    def update_leaderboard():
        leaderboard_list.delete(0, tk.END)
        top_scores = fetch_top_scores(10)
        for entry in top_scores:
            leaderboard_list.insert(tk.END, f"{entry['name']} - {entry['score']}")

    update_leaderboard()  # Initial load

    root.mainloop()
