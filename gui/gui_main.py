import tkinter as tk
from tkinter import messagebox
import time
import random
from database.db_access import insert_score, fetch_top_scores

TIMER_DURATION = 120_000  # 2 minutes in milliseconds

class BatakGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Batak Light Reaction Game")
        self.root.attributes('-fullscreen', True)  # Fullscreen mode

        self.name_var = tk.StringVar()
        self.timer_var = tk.StringVar(value="02:00.000")
        self.score_var = tk.StringVar(value="Score: 0")

        self.running = False
        self.start_time = None
        self.timer_id = None

        self.build_layout()

    def build_layout(self):
        # Main container using horizontal split
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        # Left game panel
        self.left_frame = tk.Frame(self.main_frame, padx=40, pady=40)
        self.left_frame.pack(side='left', fill='both', expand=True)

        # Right leaderboard panel - full height
        self.right_frame = tk.Frame(self.main_frame, width=400, padx=20, pady=20, bg='white')
        self.right_frame.pack(side='right', fill='y')
        self.right_frame.pack_propagate(False)

        # ----- Left Panel -----
        tk.Label(self.left_frame, text="Timer", font=("Arial", 18)).pack(anchor='center', pady=5)
        tk.Label(self.left_frame, textvariable=self.timer_var, font=("Courier", 28), fg="blue").pack(anchor='center', pady=5)

        tk.Label(self.left_frame, text="Score", font=("Arial", 18)).pack(anchor='center', pady=5)
        tk.Label(self.left_frame, textvariable=self.score_var, font=("Arial", 24)).pack(anchor='center', pady=5)

        tk.Label(self.left_frame, text="Enter Your Name", font=("Arial", 18)).pack(anchor='center', pady=10)
        tk.Entry(self.left_frame, textvariable=self.name_var, font=("Arial", 16), width=30).pack(anchor='center')

        self.start_btn = tk.Button(self.left_frame, text="Start Game", font=("Arial", 16), command=self.start_game)
        self.start_btn.pack(pady=30)

        # ----- Right Leaderboard Panel -----
        tk.Label(self.right_frame, text="Leaderboard (Top 10)", font=("Arial", 18, "bold"), bg='white').pack(anchor='n')

        self.lb_canvas = tk.Canvas(self.right_frame, bg='white', highlightthickness=0)
        self.lb_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.lb_canvas.yview)
        self.lb_inner_frame = tk.Frame(self.lb_canvas, bg='white')

        self.lb_inner_frame.bind(
            "<Configure>",
            lambda e: self.lb_canvas.configure(scrollregion=self.lb_canvas.bbox("all"))
        )

        self.lb_canvas.create_window((0, 0), window=self.lb_inner_frame, anchor="nw")
        self.lb_canvas.configure(yscrollcommand=self.lb_scrollbar.set)

        self.lb_canvas.pack(side="left", fill="both", expand=True)
        self.lb_scrollbar.pack(side="right", fill="y")

        self.refresh_leaderboard()

    def refresh_leaderboard(self):
        for widget in self.lb_inner_frame.winfo_children():
            widget.destroy()

        leaderboard = fetch_top_scores()
        for i, entry in enumerate(leaderboard, 1):
            text = f"{i:>2}. {entry['name']:<15} {entry['score']}"
            tk.Label(self.lb_inner_frame, text=text, font=("Courier", 14), bg='white').pack(anchor='w', pady=2)

    def start_game(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name before starting.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.running = True
        self.score_var.set("Score: 0")
        self.start_time = int(time.time() * 1000)
        self.update_timer()

    def update_timer(self):
        if not self.running:
            return

        elapsed = int(time.time() * 1000) - self.start_time
        remaining = max(0, TIMER_DURATION - elapsed)

        minutes = remaining // 60000
        seconds = (remaining % 60000) // 1000
        millis = remaining % 1000
        self.timer_var.set(f"{minutes:02d}:{seconds:02d}.{millis:03d}")

        if remaining > 0:
            self.timer_id = self.root.after(50, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        self.running = False
        self.root.after_cancel(self.timer_id)

        score = random.randint(10, 100)
        self.score_var.set(f"Score: {score}")

        insert_score(self.name_var.get().strip(), score)
        self.refresh_leaderboard()

        self.start_btn.config(state=tk.NORMAL)
        self.timer_var.set("02:00.000")

def launch_gui():
    root = tk.Tk()
    app = BatakGameGUI(root)
    root.mainloop()
