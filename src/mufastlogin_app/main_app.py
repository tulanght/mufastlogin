# Module Dieu phoi chinh 
import tkinter as tk 
from tkinter import ttk 
 
class MainApp: 
    def __init__(self, root): 
        self.root = root 
        self.root.title("My New App") 
        self.root.geometry("800x600") 
 
        label = ttk.Label(root, text="Welcome to your new application") 
        label.pack(pady=20, padx=20) 
