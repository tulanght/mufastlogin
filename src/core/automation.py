# file-path: src/core/automation.py
# version: 1.0
# last-updated: 2025-07-25
# description: Handles the automation of logging into the game client.
#              It finds the game window and simulates keyboard inputs.

import pygetwindow as gw
from pynput.keyboard import Controller, Key
import time

def perform_login(account: str, password: str) -> tuple[bool, str]:
    """
    Finds the MU game window and performs the login sequence.

    Args:
        account (str): The account username.
        password (str): The account password.

    Returns:
        tuple[bool, str]: A tuple containing a boolean for success status
                          and a message string.
    """
    WINDOW_TITLE = "MU"
    keyboard = Controller()

    try:
        # 1. Find the game window
        mu_windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        if not mu_windows:
            return (False, f"Không tìm thấy cửa sổ game với tiêu đề '{WINDOW_TITLE}'.\nHãy chắc chắn rằng game đã được mở.")
        
        game_window = mu_windows[0]

        # 2. Activate the window and wait for it to be ready
        if not game_window.isActive:
            game_window.activate()
            time.sleep(0.5) # Wait half a second for the window to focus

        # 3. Perform the login keystrokes
        # Type account
        keyboard.type(account)
        time.sleep(0.1)

        # Press Tab to move to the password field
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.1)

        # Type password
        keyboard.type(password)
        time.sleep(0.1)

        # Press Enter to log in
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        return (True, f"Đã gửi thông tin đăng nhập cho tài khoản '{account}' thành công!")

    except Exception as e:
        error_message = f"Đã xảy ra lỗi không mong muốn:\n{e}"
        return (False, error_message)