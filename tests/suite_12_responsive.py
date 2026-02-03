# tests/suite_12_responsive.py
import os
import time
from selenium.webdriver.common.by import By
from config.config import Config

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 12: RESPONSIVE DESIGN")
    print("=" * 80)

    viewport_sizes = [
        (375, 667, "Mobile (iPhone SE)"),
        (414, 896, "Mobile (iPhone XR)"),
        (768, 1024, "Tablet (iPad)"),
        (1024, 768, "Tablet Landscape"),
        (1366, 768, "Desktop (Laptop)"),
        (1920, 1080, "Desktop (Full HD)"),
    ]

    for width, height, device_name in viewport_sizes:
        try:
            driver.set_window_size(width, height)
            time.sleep(1)

            product_section = driver.find_element(By.ID, "product")
            helper.test_result(
                f"Responsive: {device_name}",
                product_section.is_displayed(),
                f"{width}x{height}",
            )

            screenshot_name = f"responsive_{width}x{height}.png"
            driver.save_screenshot(
                os.path.join(Config.SCREENSHOT_DIR, screenshot_name)
            )
        except Exception as e:
            helper.test_result(f"Responsive: {device_name}", False, str(e))

    driver.maximize_window()
    time.sleep(1)
