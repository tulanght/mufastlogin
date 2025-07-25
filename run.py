# File khoi dong chinh 
import tkinter as tk 
from src.mufastlogin_app.main_app import MainApp 
 
def run_application(): 
    root = tk.Tk() 
    app = MainApp(root) 
    root.mainloop() 
 
if __name__ == "__main__": 
    run_application() 
