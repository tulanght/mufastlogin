# file-path: run.py
# version: 1.2
# last-updated: 2025-07-25
# description: Added administrator rights check before starting the app.

import tkinter as tk
from tkinter import messagebox
import ctypes
import sys
from src.mufastlogin_app.main_app import MainApp
from src.core.app_logger import log

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if not is_admin():
        log.critical("Ứng dụng không có quyền Administrator. Đang thoát.")
        messagebox.showerror("Yêu cầu quyền Administrator", 
                             "Vui lòng chạy ứng dụng với quyền Administrator để có thể tương tác với game.\n\n"
                             "Cách làm: Chuột phải vào file .cmd hoặc .py và chọn 'Run as administrator'.")
        sys.exit()

    log.info("========================================")
    log.info("====== ỨNG DỤNG KHỞI ĐỘNG (ADMIN) ======")
    log.info("========================================")
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    log.info("====== ỨNG DỤNG ĐÓNG ======")