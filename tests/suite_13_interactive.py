# tests/suite_13_interactive.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from config.config import Config

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 13: INTERACTIVE ELEMENTS")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)

        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        helper.test_result(
            "Buttons present",
            len(all_buttons) > 0,
            f"Found {len(all_buttons)} buttons",
        )

        clickable_buttons = sum(
            1 for btn in all_buttons
            if btn.is_displayed() and btn.is_enabled()
        )
        helper.test_result(
            "Buttons are clickable",
            clickable_buttons > 0,
            f"{clickable_buttons}/{len(all_buttons)} clickable",
        )

        elements_with_hover = driver.find_elements(
            By.CSS_SELECTOR, "[class*='hover:']"
        )
        helper.test_result(
            "Hover effects defined",
            len(elements_with_hover) > 0,
            f"Found {len(elements_with_hover)} elements",
        )

        # Hover pada product card
        try:
            product_section = driver.find_element(By.ID, "product")
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                product_section,
            )
            time.sleep(1)

            product_cards = driver.find_elements(By.TAG_NAME, "article")
            if product_cards:
                actions = ActionChains(driver)
                actions.move_to_element(product_cards[0]).perform()
                time.sleep(0.5)
                helper.test_result(
                    "Hover action works",
                    True,
                    "Hovered over first product card",
                )
            else:
                helper.test_result(
                    "Hover action works",
                    False,
                    "No product cards found",
                )
        except Exception:
            helper.test_result("Hover action works", False)

        # Smooth scrolling
        try:
            sections = ["product", "mitra", "investasi", "contact"]
            for section_id in sections:
                section = driver.find_element(By.ID, section_id)
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    section,
                )
                time.sleep(0.3)
            helper.test_result(
                "Smooth scroll works",
                True,
                f"Scrolled to {len(sections)} sections",
            )
        except Exception:
            helper.test_result("Smooth scroll works", False)

    except Exception as e:
        helper.test_result("Interactive elements tests", False, str(e))
