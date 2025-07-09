import csv
import os
from config import DB_PATH

def insert_score(name, score):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Leaderboard file not found. Did you call init_db()?")

    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        next_id = len(rows)

    with open(DB_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([next_id, name, score])


def fetch_top_scores(limit=10):
    with open(DB_PATH, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        entries = sorted(reader, key=lambda x: int(x['score']), reverse=True)
        return entries[:limit]

