import sqlite3
from config import DB_PATH

def init_db():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    line= " CREATE TABLE IF NOT EXISTS leaderboard (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL, score INTEGER NOT NULL);"
    cur.execute(line)
    conn.commit()
    conn.close()
