"""from database.db_init import init_db

init_db()
"""

from database.db_init import init_db
from gui.gui_main import launch_gui

def main():
    init_db()
    launch_gui()

if __name__ == "__main__":
    main()
