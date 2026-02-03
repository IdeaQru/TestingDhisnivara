# utils/screenshot_manager.py
import os
from config.config import Config

def init_screenshot_dir():
    os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)

def count_screenshots():
    if not os.path.exists(Config.SCREENSHOT_DIR):
        return 0
    return len([f for f in os.listdir(Config.SCREENSHOT_DIR) if f.endswith(".png")])
