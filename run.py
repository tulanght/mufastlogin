# file-path: run.py
# version: 3.0
# last-updated: 2025-07-26
# description: Simplified entry point, no admin rights needed.

import tkinter as tk
from src.mufastlogin_app.main_app import MainApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()