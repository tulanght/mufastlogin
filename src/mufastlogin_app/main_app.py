# file-path: src/mufastlogin_app/main_app.py
# version: 5.0
# last-updated: 2025-07-26
# description: Simplified UI for the click-to-paste helper.

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.config_manager import ConfigManager
from src.core.automation import LoginHelper

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MU Click Helper")
        self.root.geometry("400x180")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')
        self.root.attributes("-topmost", True)

        self.config_manager = ConfigManager()
        self.login_helper = None

        # UI Variables
        self.selected_account = tk.StringVar()

        self.create_widgets()
        self.load_accounts_to_ui()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Chọn tài khoản:").pack(fill=tk.X)
        self.account_combobox = ttk.Combobox(
            main_frame, 
            textvariable=self.selected_account, 
            state="readonly",
            font=('Arial', 10)
        )
        self.account_combobox.pack(fill=tk.X, ipady=4, pady=5)

        self.action_button = ttk.Button(
            main_frame, 
            text="Bắt đầu Đăng nhập", 
            command=self.toggle_login_helper
        )
        self.action_button.pack(fill=tk.X, ipady=5, pady=5)

        self.status_label = ttk.Label(main_frame, text="Trạng thái: Sẵn sàng", font=('Arial', 9), foreground="blue")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))

    def load_accounts_to_ui(self):
        accounts = self.config_manager.get_all_accounts()
        self.account_combobox['values'] = accounts
        if accounts:
            self.account_combobox.current(0)

    def update_status(self, message):
        self.status_label.config(text=f"Trạng thái: {message}")
        self.root.update_idletasks()
        
    def on_helper_complete(self):
        """Callback được gọi khi helper hoàn thành nhiệm vụ."""
        self.login_helper = None
        self.action_button.config(text="Bắt đầu Đăng nhập")

    def toggle_login_helper(self):
        if self.login_helper:
            # Nếu đang chạy, dừng lại
            self.login_helper.stop()
            self.update_status("Đã dừng.")
        else:
            # Nếu chưa chạy, bắt đầu
            account = self.selected_account.get()
            if not account:
                messagebox.showwarning("Lỗi", "Vui lòng chọn một tài khoản.")
                return
            
            password = self.config_manager.get_password(account)
            
            self.action_button.config(text="Dừng Lại")
            self.login_helper = LoginHelper(
                account=account,
                password=password,
                on_state_change=self.update_status,
                on_complete=self.on_helper_complete
            )
            self.login_helper.start()