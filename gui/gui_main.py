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
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='orange')

        self.name_var = tk.StringVar()
        self.timer_var = tk.StringVar(value="02:00.000")
        self.score_var = tk.StringVar(value="0")

        self.running = False
        self.start_time = None
        self.timer_id = None

        self.build_layout()

    def build_layout(self):
        # --- Main Body Frame (no top bar) ---
        body_frame = tk.Frame(self.root, bg='orange')
        body_frame.pack(fill='both', expand=True)

        # --- Left Game Area ---
        self.left_frame = tk.Frame(body_frame, padx=60, pady=40, bg='orange')
        self.left_frame.pack(side='left', fill='both', expand=True)

        # --- Right Leaderboard Area (fully top-right aligned) ---
        self.right_frame = tk.Frame(body_frame, width=500, padx=20, pady=20, bg='white')
        self.right_frame.pack(side='right', fill='y')
        self.right_frame.pack_propagate(False)

        # --- Club Name Row: AUTO VIT (side by side, top-left) ---
        club_label_frame = tk.Frame(self.left_frame, bg='orange')
        club_label_frame.pack(anchor='w', pady=(0, 30))  # 30px space below

        auto_label = tk.Label(club_label_frame, text="AUTO", font=("Arial", 28, "bold"), fg="red", bg="orange")
        vit_label = tk.Label(club_label_frame, text="VIT", font=("Arial", 28, "bold"), fg="black", bg="orange")
        auto_label.pack(side='left')
        vit_label.pack(side='left')

        # --- Timer and Score ---
        timer_score_row = tk.Frame(self.left_frame, bg='orange')
        timer_score_row.pack(pady=40)

        tk.Label(timer_score_row, text="🏁 TIMER", font=("Arial", 22, "bold"), bg='orange').grid(row=0, column=0,
                                                                                                padx=20)
        tk.Label(timer_score_row, textvariable=self.timer_var, font=("Courier", 26), fg="blue", bg='orange').grid(row=1,
                                                                                                                  column=0,
                                                                                                                  padx=20)

        tk.Label(timer_score_row, text="🎯 SCORE", font=("Arial", 22, "bold"), bg='orange').grid(row=0, column=1,
                                                                                                padx=20)
        tk.Label(timer_score_row, textvariable=self.score_var, font=("Arial", 26), bg='orange').grid(row=1, column=1,
                                                                                                     padx=20)

        # --- Name Entry ---
        tk.Label(self.left_frame, text="🧑‍💻 Enter Your Name", font=("Arial", 20), bg='orange').pack(pady=(60, 10))
        tk.Entry(self.left_frame, textvariable=self.name_var, font=("Arial", 18), width=28).pack()

        # --- Start Button ---
        self.start_btn = tk.Button(self.left_frame, text="🚀 Start Game", font=("Arial", 18), command=self.start_game)
        self.start_btn.pack(pady=50)

        # --- Leaderboard Header ---
        tk.Label(self.right_frame, text="🏆 Leaderboard (Top 10)", font=("Arial", 20, "bold"), bg='white').pack(
            anchor='n', pady=(0, 15))

        # --- Scrollable Leaderboard Area ---
        self.lb_canvas = tk.Canvas(self.right_frame, bg='white', width=480, highlightthickness=0)
        self.lb_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.lb_canvas.yview)
        self.lb_inner_frame = tk.Frame(self.lb_canvas, bg='white')

        self.lb_inner_frame.bind("<Configure>",
                                 lambda e: self.lb_canvas.configure(scrollregion=self.lb_canvas.bbox("all")))
        self.lb_canvas.create_window((0, 0), window=self.lb_inner_frame, anchor="nw")
        self.lb_canvas.configure(yscrollcommand=self.lb_scrollbar.set)

        self.lb_canvas.pack(side="left", fill="both", expand=True)
        self.lb_scrollbar.pack(side="right", fill="y")

        self.refresh_leaderboard()
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def refresh_leaderboard(self):
        for widget in self.lb_inner_frame.winfo_children():
            widget.destroy()

        leaderboard = fetch_top_scores()
        for i, entry in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else " "
            # Format: Medal  Rank. Name         Score
            text = f"{medal} {i:>2}. {entry['name']:<14}  {entry['score']}"
            label = tk.Label(
                self.lb_inner_frame,
                text=text,
                font=("Courier New", 18),
                bg='white',
                anchor='w',
                justify='left'
            )
            label.pack(fill='x', padx=15, pady=10)

    def start_game(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name before starting.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.running = True
        self.score_var.set("0")
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

        score = random.randint(10, 999)  # simulate 3-digit scores
        self.score_var.set(f"{score}")

        insert_score(self.name_var.get().strip(), score)
        self.refresh_leaderboard()

        self.start_btn.config(state=tk.NORMAL)
        self.timer_var.set("02:00.000")

def launch_gui():
    root = tk.Tk()
    app = BatakGameGUI(root)
    root.mainloop()
