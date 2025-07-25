# file-path: src/mufastlogin_app/main_app.py
# Nội dung mới hoàn toàn

import tkinter as tk
from tkinter import ttk, messagebox
from src.core.config_manager import ConfigManager
from src.core.automation import perform_login
from pynput import keyboard
import pyautogui
import pygetwindow as gw
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MU Fast Login v1.2")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

        self.config_manager = ConfigManager()
        self.listener = None

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        self.login_tab = ttk.Frame(self.notebook, padding="10")
        self.manage_tab = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.login_tab, text="Đăng Nhập")
        self.notebook.add(self.manage_tab, text="Quản lý & Hiệu chỉnh")

        self.create_login_tab_widgets()
        self.create_manage_tab_widgets()
        self.refresh_all_account_lists()

    def create_login_tab_widgets(self):
        self.selected_account = tk.StringVar()
        ttk.Label(self.login_tab, text="Chọn tài khoản:").pack(fill=tk.X, pady=5)
        self.account_combobox = ttk.Combobox(self.login_tab, textvariable=self.selected_account, state="readonly")
        self.account_combobox.pack(fill=tk.X, ipady=4)
        self.login_button = ttk.Button(self.login_tab, text="Đăng Nhập", command=self.handle_login)
        self.login_button.pack(fill=tk.X, pady=(15, 5), ipady=4)
        self.login_status_label = ttk.Label(self.login_tab, text="Sẵn sàng...", anchor=tk.W)
        self.login_status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))

    def create_manage_tab_widgets(self):
        list_frame = ttk.Frame(self.manage_tab)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        form_frame = ttk.Frame(self.manage_tab)
        form_frame.pack(side=tk.RIGHT, fill=tk.X)

        ttk.Label(list_frame, text="Danh sách tài khoản:").pack(anchor=tk.W)
        self.account_tree = ttk.Treeview(list_frame, columns=("account"), show="headings", height=8)
        self.account_tree.heading("account", text="Tên tài khoản")
        self.account_tree.pack(fill=tk.BOTH, expand=True)
        self.account_tree.bind('<<TreeviewSelect>>', self.handle_treeview_select)

        self.account_entry_var = tk.StringVar()
        self.password_entry_var = tk.StringVar()
        ttk.Label(form_frame, text="Tài khoản:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.account_entry_var).pack(anchor=tk.W)
        ttk.Label(form_frame, text="Mật khẩu:").pack(anchor=tk.W, pady=(10,0))
        ttk.Entry(form_frame, textvariable=self.password_entry_var, show="*").pack(anchor=tk.W)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="Thêm / Cập nhật", command=self.handle_add_update).pack(fill=tk.X)
        ttk.Button(button_frame, text="Xóa", command=self.handle_delete).pack(fill=tk.X, pady=2)
        
        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=10)
        
        self.calibration_status_label = ttk.Label(form_frame, text="Trạng thái: ...")
        self.calibration_status_label.pack(anchor=tk.W)
        
        ttk.Button(form_frame, text="Hiệu chỉnh 'Account'", command=lambda: self.start_calibration('account')).pack(fill=tk.X, pady=(5,0))
        ttk.Button(form_frame, text="Hiệu chỉnh 'Password'", command=lambda: self.start_calibration('password')).pack(fill=tk.X)
        self.update_calibration_status()

    def handle_login(self):
        coords = self.config_manager.load_coords()
        if not coords or 'account' not in coords or 'password' not in coords:
            messagebox.showerror("Lỗi", "Bạn cần hiệu chỉnh tọa độ của cả Account và Password trước khi đăng nhập.")
            return

        account = self.selected_account.get()
        if not account:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một tài khoản.")
            return
            
        password = self.config_manager.get_password(account)
        user_response = messagebox.askokcancel("Hành động", "Chuẩn bị đăng nhập!\n\nHãy bấm vào cửa sổ game MU, sau đó bấm OK.")
        if user_response:
            self.login_status_label.config(text=f"Đang gửi thông tin cho '{account}'...")
            self.root.update_idletasks()
            success, message = perform_login(account, password, coords)
            self.login_status_label.config(text=message)
            if not success:
                messagebox.showerror("Lỗi Tự động hóa", message)

    def start_calibration(self, field_name):
        if self.listener and self.listener.is_alive():
            messagebox.showwarning("Đang hiệu chỉnh", "Một quá trình hiệu chỉnh khác đang chạy. Vui lòng hoàn tất hoặc khởi động lại ứng dụng.")
            return

        self.calibration_window = tk.Toplevel(self.root)
        self.calibration_window.title("Đang hiệu chỉnh...")
        self.calibration_window.geometry("400x100")
        self.calibration_window.resizable(False, False)
        self.root.eval(f'tk::PlaceWindow {str(self.calibration_window)} center')
        self.calibration_window.attributes("-topmost", True)
        
        label_text = f"Hãy di chuyển chuột đến giữa ô '{field_name.capitalize()}'\nvà nhấn phím F8 để lưu tọa độ."
        ttk.Label(self.calibration_window, text=label_text, font=("Arial", 10)).pack(pady=20)
        
        self.listener = keyboard.Listener(on_press=self.on_press_f8(field_name))
        self.listener.start()

    def on_press_f8(self, field_name):
        def on_press(key):
            try:
                if key == keyboard.Key.f8:
                    # Tìm cửa sổ game ngay tại thời điểm hiệu chỉnh
                    OUR_APP_TITLE_KEYWORD = "Fast Login"
                    WINDOW_TITLE = "MU"
                    all_mu_windows = gw.getWindowsWithTitle(WINDOW_TITLE)
                    game_window = next((w for w in all_mu_windows if OUR_APP_TITLE_KEYWORD not in w.title), None)

                    if not game_window:
                        self.calibration_window.after(100, lambda: messagebox.showerror("Lỗi", "Không tìm thấy cửa sổ game MU để hiệu chỉnh.", parent=self.calibration_window))
                        self.calibration_window.after(200, self.calibration_window.destroy)
                        self.listener.stop()
                        return

                    # Lấy tọa độ tuyệt đối
                    mouse_pos = pyautogui.position()
                    window_pos = game_window.topleft
                    
                    # Tính tọa độ tương đối
                    relative_coords = (mouse_pos[0] - window_pos[0], mouse_pos[1] - window_pos[1])
                    
                    self.config_manager.save_coords(field_name, relative_coords)
                    self.calibration_window.after(100, lambda: messagebox.showinfo("Thành công", f"Đã lưu tọa độ tương đối cho '{field_name}': {relative_coords}", parent=self.calibration_window))
                    self.calibration_window.after(200, self.calibration_window.destroy)
                    self.update_calibration_status()
                    self.listener.stop()
            except Exception as e:
                pass # Bỏ qua lỗi
        return on_press

    def update_calibration_status(self):
        coords = self.config_manager.load_coords()
        if coords and 'account' in coords and 'password' in coords:
            self.calibration_status_label.config(text="Trạng thái: Đã hiệu chỉnh", foreground="green")
        else:
            self.calibration_status_label.config(text="Trạng thái: Cần hiệu chỉnh", foreground="red")
            
    # Các hàm handle_treeview_select, handle_add_update, v.v... giữ nguyên
    # Bạn có thể copy từ phiên bản trước
    def refresh_all_account_lists(self):
        accounts = self.config_manager.get_all_accounts()
        self.account_combobox['values'] = accounts
        if accounts: self.account_combobox.current(0)
        else: self.selected_account.set('')
        for i in self.account_tree.get_children(): self.account_tree.delete(i)
        for acc in accounts: self.account_tree.insert("", tk.END, values=(acc,))
        self.update_calibration_status()

    def handle_treeview_select(self, event):
        selected_items = self.account_tree.selection()
        if selected_items:
            selected_account = self.account_tree.item(selected_items[0])['values'][0]
            password = self.config_manager.get_password(selected_account)
            self.account_entry_var.set(selected_account)
            self.password_entry_var.set(password)
    
    def handle_add_update(self):
        account = self.account_entry_var.get().strip()
        if not account:
            messagebox.showerror("Lỗi", "Tên tài khoản không được để trống.")
            return
        password = self.password_entry_var.get()
        self.config_manager.save_account(account, password)
        messagebox.showinfo("Thành công", f"Đã lưu tài khoản '{account}' thành công.")
        self.refresh_all_account_lists()

    def handle_delete(self):
        selected_items = self.account_tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn một tài khoản để xóa.")
            return
        selected_account = self.account_tree.item(selected_items[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa tài khoản '{selected_account}'?"):
            self.config_manager.delete_account(selected_account)
            self.refresh_all_account_lists()