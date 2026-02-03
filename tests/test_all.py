# tests/test_all.py
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from config.config import Config
from utils.driver_factory import DriverFactory
from utils.test_helpers import TestStats, TestHelper
from utils.screenshot_manager import init_screenshot_dir, count_screenshots

from pages.base_page import BasePage
from pages.product_section import ProductSection
from pages.kemitraan_section import KemitraanSection
from pages.investasi_section import InvestasiSection
from pages.contact_section import ContactSection


def main():
    stats = TestStats()
    driver = DriverFactory.get_driver()
    helper = TestHelper(stats, driver)

    print("=" * 80)
    print("🧪 DHISNIVARA.ID - OOP POM TEST SUITE")
    print("=" * 80)
    print(f"Testing URL: {Config.BASE_URL}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    init_screenshot_dir()

    base = BasePage(driver)
    base.open(Config.BASE_URL).wait_for_ready()
    time.sleep(2)

    # === TEST 1: PAGE LOAD & BASIC INFO ===
    try:
        current_url = driver.current_url
        helper.test_result("Page loads successfully", Config.BASE_URL in current_url, f"URL: {current_url}")

        title = driver.title
        helper.test_result("Page has title", "Dhisnivara" in title, f"Title: {title}")

        nav_start = driver.execute_script("return window.performance.timing.navigationStart")
        load_end = driver.execute_script("return window.performance.timing.loadEventEnd")
        if load_end > 0:
            load_time = (load_end - nav_start) / 1000
            helper.test_result("Page load time < 5s", load_time < 5, f"{load_time:.2f} seconds")

        ready_state = driver.execute_script("return document.readyState")
        helper.test_result("Page ready state complete", ready_state == "complete", f"State: {ready_state}")
    except Exception as e:
        helper.test_result("Page load & basic info", False, str(e))

    # === TEST 3: PRODUCT SECTION ===
    try:
        product = ProductSection(driver)
        section = product.get_section()

        # Heading
        try:
            h2 = section.find_element(By.CSS_SELECTOR, "h2")
            helper.test_result("Product section has heading", h2.is_displayed(), h2.text[:50])
        except:
            helper.test_result("Product section has heading", False)

        # Description
        try:
            p = section.find_element(By.TAG_NAME, "p")
            helper.test_result("Product section has description", len(p.text) > 0)
        except:
            helper.test_result("Product section has description", False)

        cards = product.get_product_cards()
        helper.test_result("Product cards >= 4", len(cards) >= 4, f"Found {len(cards)} cards")

        names = product.get_product_names()
        for expected in Config.EXPECTED_PRODUCTS:
            helper.test_result(f"Product exists: {expected}", any(expected in n for n in names))

        helper.test_result("Product badges present >=4", product.get_badges_count() >= 4)
        helper.test_result("Product descriptions present >=4", product.get_descriptions_count() >= 4)
        helper.test_result("Product images loaded >=4", product.get_loaded_images_count() >= 4)

        # Tab switching
        initial = product.get_product_names()
        product.click_cooked_tab()
        time.sleep(2)
        new = product.get_product_names()
        helper.test_result("Tab switching changes products", initial != new)
        product.click_fresh_tab()
        time.sleep(1)

        helper.take_screenshot("03_product_section.png")

    except Exception as e:
        helper.test_result("Product section tests", False, str(e))

    # === TEST 4: KEMITRAAN SECTION ===
    try:
        mitra = KemitraanSection(driver)
        section = mitra.get_section()

        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Kemitraan section has heading", h2.is_displayed())
        except:
            helper.test_result("Kemitraan section has heading", False)

        feature_status = mitra.has_all_features()
        for feat, ok in feature_status.items():
            helper.test_result(f"Feature mentioned: {feat}", ok)

        helper.take_screenshot("04_kemitraan_section.png")
    except Exception as e:
        helper.test_result("Kemitraan section tests", False, str(e))

    # === TEST 7: INVESTASI SECTION (ringkas) ===
    try:
        inv = InvestasiSection(driver)
        section = inv.get_section()
        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Investasi section has heading", h2.is_displayed())
        except:
            helper.test_result("Investasi section has heading", False)

        tables = inv.get_tables()
        helper.test_result("Investment table exists", len(tables) > 0, f"{len(tables)} table(s)")

        text = inv.get_text()
        helper.test_result("ROI % mentioned", "12" in text and "%" in text)
    except Exception as e:
        helper.test_result("Investasi section tests", False, str(e))

    # === TEST 8: CONTACT SECTION (ringkas) ===
    try:
        contact = ContactSection(driver)
        section = contact.get_section()
        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Contact section has heading", h2.is_displayed())
        except:
            helper.test_result("Contact section has heading", False)

        txt = contact.text()
        src = contact.page_source()

        helper.test_result("Phone number present", Config.PHONE_NUMBER in src or "811-359-0718" in src)
        helper.test_result("Email address present", Config.EMAIL in src or "@dhisnivara" in src)
        helper.test_result("Physical address present", "Malang" in txt and "Jawa Timur" in txt)

        helper.take_screenshot("08_contact_section.png")
    except Exception as e:
        helper.test_result("Contact section tests", False, str(e))

    # === FINAL SUMMARY ===
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
