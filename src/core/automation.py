# file-path: src/core/automation.py
# version: 5.0
# last-updated: 2025-07-26
# description: Implements the click-to-paste listener logic.

from pynput import mouse, keyboard
import time

class LoginHelper:
    def __init__(self, account, password, on_state_change, on_complete):
        self.account = account
        self.password = password
        self.on_state_change = on_state_change # Callback để cập nhật UI
        self.on_complete = on_complete         # Callback khi hoàn thành
        
        self.keyboard = keyboard.Controller()
        self.listener = None
        self.click_count = 0

    def on_click(self, x, y, button, pressed):
        # Chỉ hành động khi chuột được nhả ra
        if button == mouse.Button.left and not pressed:
            self.click_count += 1
            
            if self.click_count == 1:
                # Click lần 1: Gõ tài khoản
                self.on_state_change("Đã nhận click 1. Đang gõ tài khoản...")
                time.sleep(0.1) # Thêm một khoảng nghỉ nhỏ
                self.keyboard.type(self.account)
                self.on_state_change("Gõ tài khoản xong. Chờ click vào ô Password...")
            
            elif self.click_count == 2:
                # Click lần 2: Gõ mật khẩu và kết thúc
                self.on_state_change("Đã nhận click 2. Đang gõ mật khẩu...")
                time.sleep(0.1)
                self.keyboard.type(self.password)
                self.on_state_change("Hoàn thành! Bạn hãy tự nhấn Enter.")
                
                # Dừng lắng nghe và gọi callback hoàn thành
                self.stop()
                return False

    def start(self):
        # Chỉ tạo một listener duy nhất
        if not self.listener:
            self.on_state_change("Đang chờ click vào ô Account...")
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
            self.on_complete()