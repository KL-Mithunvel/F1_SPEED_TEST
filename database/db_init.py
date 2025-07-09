import os
import csv
from config import DB_PATH

def init_db():
    if not os.path.isfile(DB_PATH):
        try:
            with open(DB_PATH, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "name", "score"])
            print(f"Created new leaderboard file: {DB_PATH}")
        except Exception as e:
            print(f"[ERROR] Failed to create CSV: {e}")
    else:
        print(f"Leaderboard file already exists at: {DB_PATH}")
