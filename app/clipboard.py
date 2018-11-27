import time
import threading
import pyperclip


class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, interval=0.5):
        super().__init__(daemon=True)
        self._callback = callback
        self._interval = interval
        self._running = False
        self._last_content = None

    def run(self):
        self._running = True
        self._last_content = pyperclip.paste()
        while self._running:
            current_content = pyperclip.paste()
            if current_content != self._last_content:
                self._callback(current_content)
                self._last_content = current_content
            time.sleep(self._interval)

    def stop(self):
        self._running = False

