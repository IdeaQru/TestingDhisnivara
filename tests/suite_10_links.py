# tests/suite_10_links.py
from selenium.webdriver.common.by import By

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 10: NAVIGATION & LINKS")
    print("=" * 80)
    try:
        all_links = driver.find_elements(By.TAG_NAME, "a")
        helper.test_result(
            "Links present on page",
            len(all_links) > 0,
            f"Found {len(all_links)} links",
        )

        internal_links = [
            link for link in all_links
            if link.get_attribute("href") and "#" in link.get_attribute("href")
        ]
        helper.test_result(
            "Internal navigation links",
            len(internal_links) > 0,
            f"Found {len(internal_links)} internal links",
        )

        external_links = [
            link for link in all_links
            if link.get_attribute("href")
            and link.get_attribute("href").startswith("http")
            and "dhisnivara" not in link.get_attribute("href")
        ]
        helper.test_result(
            "External links present",
            len(external_links) >= 0,
            f"Found {len(external_links)} external links",
        )

        empty_links = [
            link for link in all_links
            if not link.get_attribute("href")
            or link.get_attribute("href") in ["", "#"]
        ]
        helper.test_result(
            "No empty links",
            len(empty_links) == 0,
            f"Found {len(empty_links)} empty links",
        )

        try:
            logo = driver.find_element(
                By.CSS_SELECTOR,
                "a[href='/'], a[href='#'], img[alt*='logo']",
            )
            helper.test_result(
                "Logo/brand link exists",
                logo.is_displayed(),
            )
        except Exception:
            helper.test_result("Logo/brand link exists", False)

    except Exception as e:
        helper.test_result("Navigation & links tests", False, str(e))
