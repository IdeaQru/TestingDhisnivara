# tests/suite_14_seo.py
import time
from selenium.webdriver.common.by import By
from config.config import Config

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 14: SEO & ACCESSIBILITY")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)

        # Meta description
        try:
            meta_desc = driver.find_element(
                By.CSS_SELECTOR, "meta[name='description']"
            )
            desc_content = meta_desc.get_attribute("content")
            helper.test_result(
                "Meta description exists",
                bool(desc_content),
                f"Length: {len(desc_content) if desc_content else 0}",
            )
        except Exception:
            helper.test_result("Meta description exists", False)

        # Open Graph
        try:
            og_tags = driver.find_elements(
                By.CSS_SELECTOR, "meta[property^='og:']"
            )
            helper.test_result(
                "Open Graph tags present",
                len(og_tags) > 0,
                f"Found {len(og_tags)} OG tags",
            )
        except Exception:
            helper.test_result("Open Graph tags present", False)

        # Heading hierarchy
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        helper.test_result(
            "H1 tag present",
            len(h1_tags) >= 1,
            f"Found {len(h1_tags)} H1 tag(s)",
        )
        helper.test_result(
            "Only one H1 tag",
            len(h1_tags) == 1,
            "SEO best practice",
        )

        h2_tags = driver.find_elements(By.TAG_NAME, "h2")
        helper.test_result(
            "H2 tags present",
            len(h2_tags) > 0,
            f"Found {len(h2_tags)} H2 tags",
        )

        h3_tags = driver.find_elements(By.TAG_NAME, "h3")
        helper.test_result(
            "H3 tags present",
            len(h3_tags) > 0,
            f"Found {len(h3_tags)} H3 tags",
        )

        # Lang attribute
        html_tag = driver.find_element(By.TAG_NAME, "html")
        lang = html_tag.get_attribute("lang")
        helper.test_result(
            "Language attribute set",
            lang is not None,
            f"Language: {lang}",
        )

        # Viewport
        try:
            viewport = driver.find_element(
                By.CSS_SELECTOR, "meta[name='viewport']"
            )
            helper.test_result("Viewport meta tag exists", True)
        except Exception:
            helper.test_result("Viewport meta tag exists", False)

        # Favicon
        try:
            favicon = driver.find_element(
                By.CSS_SELECTOR, "link[rel*='icon']"
            )
            helper.test_result("Favicon exists", True)
        except Exception:
            helper.test_result("Favicon exists", False)

    except Exception as e:
        helper.test_result("SEO & accessibility tests", False, str(e))
