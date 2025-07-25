# file-path: src/mufastlogin_app/main_app.py
# version: 1.0
# last-updated: 2025-07-25
# description: The main user interface for the MU Fast Login application.

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.config_manager import ConfigManager
from src.core.automation import perform_login
import os

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MU Fast Login v1.0")
        self.root.geometry("350x180")
        self.root.resizable(False, False)

        # Center the window
        self.root.eval('tk::PlaceWindow . center')

        # Initialize core components
        self.config_manager = ConfigManager()

        # UI variables
        self.selected_account = tk.StringVar()

        # Create and layout widgets
        self.create_widgets()
        self.load_accounts_to_ui()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Account selection
        ttk.Label(main_frame, text="Chọn tài khoản:").pack(fill=tk.X, pady=5)
        self.account_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.selected_account,
            state="readonly"
        )
        self.account_combobox.pack(fill=tk.X)

        # Login button
        self.login_button = ttk.Button(
            main_frame,
            text="Đăng Nhập",
            command=self.handle_login
        )
        self.login_button.pack(fill=tk.X, pady=(15, 5))

        # Status bar
        self.status_label = ttk.Label(main_frame, text="Sẵn sàng...", anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def load_accounts_to_ui(self):
        accounts = self.config_manager.get_all_accounts()
        if accounts:
            self.account_combobox['values'] = accounts
            self.account_combobox.current(0)
        else:
            self.account_combobox['values'] = []
            self.status_label.config(text="Chưa có tài khoản. Hãy tạo file settings.ini")
            # Create a sample settings.ini if it doesn't exist
            if not os.path.exists(self.config_manager.config_path):
                self.config_manager.save_account("test_account", "test_password")
                self.load_accounts_to_ui() # Reload

    def handle_login(self):
        account = self.selected_account.get()
        if not account:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một tài khoản.")
            return

        password = self.config_manager.get_password(account)

        # Prompt user to focus the game window, as requested
        user_response = messagebox.askokcancel(
            "Hành động",
            "Chuẩn bị đăng nhập!\n\nHãy bấm vào cửa sổ game MU, sau đó bấm OK."
        )

        if user_response: # If user clicks OK
            self.status_label.config(text=f"Đang gửi thông tin cho '{account}'...")
            self.root.update_idletasks() # Refresh UI to show the message
            
            success, message = perform_login(account, password)
            
            self.status_label.config(text=message)
            if not success:
                messagebox.showerror("Lỗi Tự động hóa", message)