# file-path: src/core/automation.py
# Nội dung mới hoàn toàn

import pygetwindow as gw
from pynput.keyboard import Controller, Key
import win32api
import win32con
import time
from src.core.app_logger import log

def low_level_click(x, y):
    """Performs a low-level mouse click using win32api."""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def perform_login(account: str, password: str, relative_coords: dict) -> tuple[bool, str]:
    OUR_APP_TITLE_KEYWORD = "Fast Login"
    WINDOW_TITLE = "MU"
    
    if not relative_coords or 'account' not in relative_coords or 'password' not in relative_coords:
        return (False, "Chưa hiệu chỉnh tọa độ. Vui lòng vào tab Quản lý.")

    keyboard = Controller()
    try:
        log.info("--- Bắt đầu quá trình đăng nhập (Hybrid: Win32 Click + Pynput Type) ---")
        
        all_mu_windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        game_window = next((w for w in all_mu_windows if OUR_APP_TITLE_KEYWORD not in w.title), None)
        if not game_window:
            return (False, "Không tìm thấy cửa sổ game.")

        game_window.activate()
        time.sleep(0.5)
        
        window_pos = game_window.topleft
        log.info(f"Tọa độ góc cửa sổ game hiện tại: {window_pos}")

        account_click_pos = (window_pos[0] + relative_coords['account'][0], window_pos[1] + relative_coords['account'][1])
        log.info(f"Click (low-level) vào ô Account tại tọa độ: {account_click_pos}")
        low_level_click(account_click_pos[0], account_click_pos[1])
        time.sleep(0.3)
        log.info(f"Gõ (pynput) tài khoản: '{account}'")
        keyboard.type(account)

        password_click_pos = (window_pos[0] + relative_coords['password'][0], window_pos[1] + relative_coords['password'][1])
        log.info(f"Click (low-level) vào ô Password tại tọa độ: {password_click_pos}")
        low_level_click(password_click_pos[0], password_click_pos[1])
        time.sleep(0.3)
        log.info("Gõ (pynput) mật khẩu.")
        keyboard.type(password)

        log.info("Nhấn (pynput) phím ENTER.")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        
        log.info("--- Quá trình đăng nhập tự động kết thúc ---")
        return (True, "Đã gửi thông tin đăng nhập thành công!")
    except Exception as e:
        log.error(f"Lỗi khi thực hiện đăng nhập: {e}", exc_info=True)
        return (False, f"Lỗi trong quá trình tự động hóa:\n{e}")