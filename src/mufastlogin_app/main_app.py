# file-path: src/mufastlogin_app/main_app.py
# version: 1.1
# last-updated: 2025-07-25
# description: The main UI, refactored to use a tabbed interface for login
#              and account management.

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.config_manager import ConfigManager
from src.core.automation import perform_login
import os

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MU Fast Login v1.1")
        self.root.geometry("400x300") # Increased size for new tab
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

        self.config_manager = ConfigManager()

        # Create the Tab control
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Create Frames for each tab
        self.login_tab = ttk.Frame(self.notebook, padding="10")
        self.manage_tab = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.login_tab, text="Đăng Nhập")
        self.notebook.add(self.manage_tab, text="Quản lý Tài khoản")

        # Populate tabs with widgets
        self.create_login_tab_widgets()
        self.create_manage_tab_widgets()

        # Load initial data
        self.refresh_all_account_lists()

    def create_login_tab_widgets(self):
        # UI variables
        self.selected_account = tk.StringVar()

        # Widgets
        ttk.Label(self.login_tab, text="Chọn tài khoản:").pack(fill=tk.X, pady=5)
        self.account_combobox = ttk.Combobox(
            self.login_tab,
            textvariable=self.selected_account,
            state="readonly"
        )
        self.account_combobox.pack(fill=tk.X, ipady=4)

        self.login_button = ttk.Button(
            self.login_tab,
            text="Đăng Nhập",
            command=self.handle_login
        )
        self.login_button.pack(fill=tk.X, pady=(15, 5), ipady=4)

        self.login_status_label = ttk.Label(self.login_tab, text="Sẵn sàng...", anchor=tk.W)
        self.login_status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))


    def create_manage_tab_widgets(self):
        # Left frame for list
        list_frame = ttk.Frame(self.manage_tab)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right frame for entries and buttons
        form_frame = ttk.Frame(self.manage_tab)
        form_frame.pack(side=tk.RIGHT, fill=tk.X)

        # Account List
        ttk.Label(list_frame, text="Danh sách tài khoản:").pack(anchor=tk.W)
        self.account_tree = ttk.Treeview(list_frame, columns=("account"), show="headings", height=8)
        self.account_tree.heading("account", text="Tên tài khoản")
        self.account_tree.pack(fill=tk.BOTH, expand=True)
        self.account_tree.bind('<<TreeviewSelect>>', self.handle_treeview_select)

        # Form entries
        self.account_entry_var = tk.StringVar()
        self.password_entry_var = tk.StringVar()

        ttk.Label(form_frame, text="Tài khoản:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.account_entry_var).pack(anchor=tk.W)

        ttk.Label(form_frame, text="Mật khẩu:").pack(anchor=tk.W, pady=(10,0))
        ttk.Entry(form_frame, textvariable=self.password_entry_var, show="*").pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(button_frame, text="Thêm / Cập nhật", command=self.handle_add_update).pack(fill=tk.X, ipady=2)
        ttk.Button(button_frame, text="Xóa", command=self.handle_delete).pack(fill=tk.X, pady=5, ipady=2)
        ttk.Button(button_frame, text="Làm mới", command=self.clear_form).pack(fill=tk.X, ipady=2)

    def refresh_all_account_lists(self):
        accounts = self.config_manager.get_all_accounts()
        
        # Refresh login tab combobox
        self.account_combobox['values'] = accounts
        if accounts:
            self.account_combobox.current(0)
            self.login_status_label.config(text="Sẵn sàng...")
        else:
            self.selected_account.set('')
            self.login_status_label.config(text="Chưa có tài khoản. Hãy thêm ở tab Quản lý.")

        # Refresh management tab treeview
        for i in self.account_tree.get_children(): # Clear existing list
            self.account_tree.delete(i)
        for acc in accounts: # Repopulate
            self.account_tree.insert("", tk.END, values=(acc,))

    def handle_login(self):
        account = self.selected_account.get()
        if not account:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một tài khoản.")
            return
        password = self.config_manager.get_password(account)
        user_response = messagebox.askokcancel("Hành động", "Chuẩn bị đăng nhập!\n\nHãy bấm vào cửa sổ game MU, sau đó bấm OK.")
        if user_response:
            self.login_status_label.config(text=f"Đang gửi thông tin cho '{account}'...")
            self.root.update_idletasks()
            success, message = perform_login(account, password)
            self.login_status_label.config(text=message)
            if not success:
                messagebox.showerror("Lỗi Tự động hóa", message)

    def handle_treeview_select(self, event):
        selected_items = self.account_tree.selection()
        if selected_items:
            selected_account = self.account_tree.item(selected_items[0])['values'][0]
            password = self.config_manager.get_password(selected_account)
            self.account_entry_var.set(selected_account)
            self.password_entry_var.set(password)

    def handle_add_update(self):
        account = self.account_entry_var.get().strip()
        password = self.password_entry_var.get()
        if not account:
            messagebox.showerror("Lỗi", "Tên tài khoản không được để trống.")
            return
        self.config_manager.save_account(account, password)
        messagebox.showinfo("Thành công", f"Đã lưu tài khoản '{account}' thành công.")
        self.refresh_all_account_lists()
        self.clear_form()

    def handle_delete(self):
        selected_items = self.account_tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn một tài khoản để xóa.")
            return
        
        selected_account = self.account_tree.item(selected_items[0])['values'][0]
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa tài khoản '{selected_account}'?"):
            self.config_manager.delete_account(selected_account)
            messagebox.showinfo("Thành công", f"Đã xóa tài khoản '{selected_account}'.")
            self.refresh_all_account_lists()
            self.clear_form()

    def clear_form(self):
        self.account_entry_var.set("")
        self.password_entry_var.set("")
        self.account_tree.selection_remove(self.account_tree.selection())