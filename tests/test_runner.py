# tests/test_runner.py
import time
import os

from config.config import Config
from utils.driver_factory import DriverFactory
from utils.test_helpers import TestStats, TestHelper
from utils.screenshot_manager import init_screenshot_dir, count_screenshots
from pages.base_page import BasePage

from tests import (
    suite_01_page_basic,
    suite_02_sections,
    suite_03_product,
    suite_04_kemitraan,
    suite_05_iot,
    suite_06_lokasi,
    suite_07_investasi,
    suite_08_contact,
    suite_09_whatsapp,
    suite_10_links,
    suite_11_images,
    suite_12_responsive,
    suite_13_interactive,
    suite_14_seo,
    suite_15_performance,
    suite_16_business,
)


def main():
    stats = TestStats()
    driver = DriverFactory.get_driver()
    helper = TestHelper(stats, driver)

    print("=" * 80)
    print("🧪 DHISNIVARA.ID - OOP POM TEST SUITE (FULL, MODULAR)")
    print("=" * 80)
    print(f"Testing URL: {Config.BASE_URL}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    init_screenshot_dir()

    base = BasePage(driver)
    base.open(Config.BASE_URL).wait_for_ready()
    time.sleep(2)

    # Panggil semua suite berurutan
    suite_01_page_basic.run_suite(driver, helper)
    suite_02_sections.run_suite(driver, helper)
    suite_03_product.run_suite(driver, helper)
    suite_04_kemitraan.run_suite(driver, helper)
    suite_05_iot.run_suite(driver, helper)
    suite_06_lokasi.run_suite(driver, helper)
    suite_07_investasi.run_suite(driver, helper)
    suite_08_contact.run_suite(driver, helper)
    suite_09_whatsapp.run_suite(driver, helper)
    suite_10_links.run_suite(driver, helper)
    suite_11_images.run_suite(driver, helper)
    suite_12_responsive.run_suite(driver, helper)
    suite_13_interactive.run_suite(driver, helper)
    suite_14_seo.run_suite(driver, helper)
    suite_15_performance.run_suite(driver, helper)
    suite_16_business.run_suite(driver, helper)

    # Summary
    print("\n" + "=" * 80)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 80)
    print(stats.summary_text())
    print("\n📸 SCREENSHOTS")
    print(f"Screenshots dir: {Config.SCREENSHOT_DIR}")
    print(f"Total screenshots: {count_screenshots()}")

    driver.get(Config.BASE_URL)
    time.sleep(2)
    driver.save_screenshot(os.path.join(Config.SCREENSHOT_DIR, "00_full_page_final.png"))

    input("\nPress Enter to close browser and exit...")
    driver.quit()


if __name__ == "__main__":
    main()
