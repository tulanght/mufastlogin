# file-path: run.py
# version: 1.0
# last-updated: 2025-07-25
# description: Entry point for the MU Fast Login application.

import tkinter as tk
from src.mufastlogin_app.main_app import MainApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()