# tests/suite_09_whatsapp.py
from selenium.webdriver.common.by import By

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 9: WHATSAPP INTEGRATION")
    print("=" * 80)
    try:
        wa_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='wa.me']")
        helper.test_result(
            "WhatsApp links present",
            len(wa_links) > 0,
            f"Found {len(wa_links)} WA links",
        )

        if wa_links:
            wa_number = "628113590718"
            correct_number_count = sum(
                1 for link in wa_links if wa_number in link.get_attribute("href")
            )
            helper.test_result(
                "WhatsApp links use correct number",
                correct_number_count == len(wa_links),
                f"{correct_number_count}/{len(wa_links)} links",
            )

            product_wa = [
                link for link in wa_links
                if "produk" in link.get_attribute("href").lower()
            ]
            helper.test_result(
                "Product-specific WA links",
                len(product_wa) > 0,
                f"{len(product_wa)} product WA links",
            )

            kemitraan_wa = [
                link for link in wa_links
                if "kemitraan" in link.get_attribute("href").lower()
            ]
            helper.test_result(
                "Kemitraan WA links",
                len(kemitraan_wa) > 0,
                f"{len(kemitraan_wa)} kemitraan WA links",
            )

            has_message = any(
                "text=" in link.get_attribute("href") for link in wa_links
            )
            helper.test_result(
                "WA links have pre-filled messages",
                has_message,
            )

            target_blank_count = sum(
                1 for link in wa_links
                if link.get_attribute("target") == "_blank"
            )
            helper.test_result(
                "WA links open in new tab",
                target_blank_count > 0,
                f"{target_blank_count}/{len(wa_links)} links with _blank",
            )

    except Exception as e:
        helper.test_result("WhatsApp integration tests", False, str(e))
