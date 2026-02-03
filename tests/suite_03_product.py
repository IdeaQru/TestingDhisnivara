import time
from selenium.webdriver.common.by import By
from config.config import Config
from pages.product_section import ProductSection

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 3: PRODUCT SECTION - DETAILED (OOP POM)")
    print("=" * 80)
    try:
        product = ProductSection(driver)
        section = product.get_section()

        # Heading
        try:
            h2 = section.find_element(By.CSS_SELECTOR, "h2")
            helper.test_result("Product section has heading", h2.is_displayed(), h2.text[:50])
        except Exception:
            helper.test_result("Product section has heading", False)

        # Description
        try:
            p = section.find_element(By.TAG_NAME, "p")
            helper.test_result("Product section has description", len(p.text) > 0)
        except Exception:
            helper.test_result("Product section has description", False)

        # Cards
        cards = product.get_product_cards()
        helper.test_result("Product cards >= 4", len(cards) >= 4, f"Found {len(cards)} cards")

        # Expected names
        names = product.get_product_names()
        for expected in Config.EXPECTED_PRODUCTS:
            helper.test_result(f"Product exists: {expected}", any(expected in n for n in names))

        helper.test_result("Product badges present >=4", product.get_badges_count() >= 4)
        helper.test_result("Product descriptions present >=4", product.get_descriptions_count() >= 4)
        helper.test_result("Product images loaded >=4", product.get_loaded_images_count() >= 4)

        # Tabs
        initial = product.get_product_names()
        product.click_cooked_tab()
        time.sleep(2)
        new = product.get_product_names()
        helper.test_result("Tab switching changes products", initial != new)
        product.click_fresh_tab()
        time.sleep(1)

        helper.test_result("'Lihat Katalog Lengkap' button exists", product.is_katalog_button_displayed())
        helper.test_result("'Hubungi Sales' button exists", product.is_sales_button_displayed())

        helper.take_screenshot("03_product_section.png")
    except Exception as e:
        helper.test_result("Product section tests", False, str(e))
