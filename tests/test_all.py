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
    print("🧪 DHISNIVARA.ID - OOP POM TEST SUITE (FULL)")
    print("=" * 80)
    print(f"Testing URL: {Config.BASE_URL}")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    init_screenshot_dir()

    base = BasePage(driver)
    base.open(Config.BASE_URL).wait_for_ready()
    time.sleep(2)

    # === TEST 1: PAGE LOAD & BASIC INFO ===
    print("\n" + "=" * 80)
    print("TEST SUITE 1: PAGE LOAD & BASIC INFORMATION")
    print("=" * 80)
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

    # === TEST 2: SECTION EXISTENCE ===
    print("\n" + "=" * 80)
    print("TEST SUITE 2: SECTION EXISTENCE & VISIBILITY")
    print("=" * 80)
    sections_to_test = {
        "product": "Product Section",
        "mitra": "Kemitraan Section",
        "kerja-sama": "Kerja Sama Section",
        "investasi": "Investasi Section",
        "contact": "Contact Section",
    }
    for section_id, section_name in sections_to_test.items():
        try:
            section = driver.find_element(By.ID, section_id)
            helper.test_result(f"{section_name} exists", section.is_displayed())
        except Exception:
            helper.test_result(f"{section_name} exists", False, "Section not found")

    # === TEST 3: PRODUCT SECTION (POM) ===
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

        # Card count
        cards = product.get_product_cards()
        helper.test_result("Product cards >= 4", len(cards) >= 4, f"Found {len(cards)} cards")

        # Expected product names
        names = product.get_product_names()
        for expected in Config.EXPECTED_PRODUCTS:
            helper.test_result(f"Product exists: {expected}", any(expected in n for n in names))

        # Badges, descriptions, images
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

        # CTA buttons
        helper.test_result("'Lihat Katalog Lengkap' button exists", product.is_katalog_button_displayed())
        helper.test_result("'Hubungi Sales' button exists", product.is_sales_button_displayed())

        helper.take_screenshot("03_product_section.png")
    except Exception as e:
        helper.test_result("Product section tests", False, str(e))

    # === TEST 4: KEMITRAAN SECTION (POM) ===
    print("\n" + "=" * 80)
    print("TEST SUITE 4: KEMITRAAN SECTION")
    print("=" * 80)
    try:
        mitra = KemitraanSection(driver)
        section = mitra.get_section()

        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Kemitraan section has heading", h2.is_displayed())
        except Exception:
            helper.test_result("Kemitraan section has heading", False)

        feature_status = mitra.has_all_features()
        for feat, ok in feature_status.items():
            helper.test_result(f"Feature mentioned: {feat}", ok)

        helper.take_screenshot("04_kemitraan_section.png")
    except Exception as e:
        helper.test_result("Kemitraan section tests", False, str(e))

    # === TEST 5: IoT MONITORING (global source) ===
    print("\n" + "=" * 80)
    print("TEST SUITE 5: IoT MONITORING")
    print("=" * 80)
    try:
        page_source = driver.page_source

        helper.test_result("Temperature data present", "24°C" in page_source or "24°" in page_source)
        helper.test_result("Humidity data present", "85%" in page_source)
        helper.test_result("System status present", "98%" in page_source or "OK" in page_source)

        iot_keywords = ["Real-time", "Monitoring", "Temperature", "Humidity", "System"]
        for keyword in iot_keywords:
            helper.test_result(f"IoT keyword: {keyword}", keyword in page_source)
    except Exception as e:
        helper.test_result("IoT monitoring tests", False, str(e))

    # === TEST 6: LOKASI KUMBUNG ===
    print("\n" + "=" * 80)
    print("TEST SUITE 6: LOKASI KUMBUNG")
    print("=" * 80)
    try:
        page_text = driver.page_source

        locations = ["Puncu", "Kediri", "Harjo Kuncaran", "Malang", "Sumbermanjing"]
        for location in locations:
            helper.test_result(f"Location mentioned: {location}", location in page_text)

        helper.test_result(
            "RT/RW information present",
            ("RT" in page_text and "RW" in page_text) or "RT 04" in page_text or "RT 06" in page_text,
        )
    except Exception as e:
        helper.test_result("Lokasi kumbung tests", False, str(e))

    # === TEST 7: INVESTASI SECTION (POM) ===
    print("\n" + "=" * 80)
    print("TEST SUITE 7: INVESTASI SECTION")
    print("=" * 80)
    try:
        inv = InvestasiSection(driver)
        section = inv.get_section()

        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Investasi section has heading", h2.is_displayed())
        except Exception:
            helper.test_result("Investasi section has heading", False)

        tables = inv.get_tables()
        helper.test_result("Investment table exists", len(tables) > 0, f"{len(tables)} table(s)")

        text = inv.get_text()
        helper.test_result("ROI % mentioned", "12" in text and "%" in text)

        # Optional: keywords investasi
        investment_keywords = ["Modal", "Return", "Tenor", "Investasi", "Keuntungan"]
        for keyword in investment_keywords:
            helper.test_result(f"Investment keyword: {keyword}", keyword in text)

        helper.take_screenshot("07_investasi_section.png")
    except Exception as e:
        helper.test_result("Investasi section tests", False, str(e))

    # === TEST 8: CONTACT SECTION (POM) ===
    print("\n" + "=" * 80)
    print("TEST SUITE 8: CONTACT SECTION")
    print("=" * 80)
    try:
        contact = ContactSection(driver)
        section = contact.get_section()

        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result("Contact section has heading", h2.is_displayed())
        except Exception:
            helper.test_result("Contact section has heading", False)

        txt = contact.text()
        src = contact.page_source()

        helper.test_result("Phone number present", Config.PHONE_NUMBER in src or "811-359-0718" in src)
        helper.test_result("Email address present", Config.EMAIL in src or "@dhisnivara" in src)
        helper.test_result("Physical address present", "Malang" in txt and "Jawa Timur" in txt)
        helper.test_result("Postal code present", "65176" in txt)

        helper.take_screenshot("08_contact_section.png")
    except Exception as e:
        helper.test_result("Contact section tests", False, str(e))

    # === TEST 9: WHATSAPP INTEGRATION ===
    print("\n" + "=" * 80)
    print("TEST SUITE 9: WHATSAPP INTEGRATION")
    print("=" * 80)
    try:
        wa_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='wa.me']")
        helper.test_result("WhatsApp links present", len(wa_links) > 0, f"Found {len(wa_links)} WA links")

        if wa_links:
            wa_number = "628113590718"
            correct_number_count = sum(1 for link in wa_links if wa_number in link.get_attribute("href"))
            helper.test_result(
                "WhatsApp links use correct number",
                correct_number_count == len(wa_links),
                f"{correct_number_count}/{len(wa_links)} links",
            )

            product_wa = [link for link in wa_links if "produk" in link.get_attribute("href").lower()]
            helper.test_result("Product-specific WA links", len(product_wa) > 0, f"{len(product_wa)} product WA links")

            kemitraan_wa = [link for link in wa_links if "kemitraan" in link.get_attribute("href").lower()]
            helper.test_result("Kemitraan WA links", len(kemitraan_wa) > 0, f"{len(kemitraan_wa)} kemitraan WA links")

            has_message = any("text=" in link.get_attribute("href") for link in wa_links)
            helper.test_result("WA links have pre-filled messages", has_message)

            target_blank_count = sum(1 for link in wa_links if link.get_attribute("target") == "_blank")
            helper.test_result("WA links open in new tab", target_blank_count > 0, f"{target_blank_count} with _blank")
    except Exception as e:
        helper.test_result("WhatsApp integration tests", False, str(e))

    # === TEST 10: NAVIGATION & LINKS ===
    print("\n" + "=" * 80)
    print("TEST SUITE 10: NAVIGATION & LINKS")
    print("=" * 80)
    try:
        all_links = driver.find_elements(By.TAG_NAME, "a")
        helper.test_result("Links present on page", len(all_links) > 0, f"Found {len(all_links)} links")

        internal_links = [link for link in all_links if link.get_attribute("href") and "#" in link.get_attribute("href")]
        helper.test_result("Internal navigation links", len(internal_links) > 0, f"{len(internal_links)} internal links")

        external_links = [
            link
            for link in all_links
            if link.get_attribute("href")
            and link.get_attribute("href").startswith("http")
            and "dhisnivara" not in link.get_attribute("href")
        ]
        helper.test_result("External links present", len(external_links) >= 0, f"{len(external_links)} external links")

        empty_links = [
            link for link in all_links if not link.get_attribute("href") or link.get_attribute("href") in ["#", ""]
        ]
        helper.test_result("No empty links", len(empty_links) == 0, f"Found {len(empty_links)} empty links")

        try:
            logo = driver.find_element(By.CSS_SELECTOR, "a[href='/'], a[href='#'], img[alt*='logo']")
            helper.test_result("Logo/brand link exists", logo.is_displayed())
        except Exception:
            helper.test_result("Logo/brand link exists", False)
    except Exception as e:
        helper.test_result("Navigation & links tests", False, str(e))

    # === TEST 11: IMAGES & MEDIA ===
    print("\n" + "=" * 80)
    print("TEST SUITE 11: IMAGES & MEDIA")
    print("=" * 80)
    try:
        all_images = driver.find_elements(By.TAG_NAME, "img")
        helper.test_result("Images present on page", len(all_images) > 0, f"Found {len(all_images)} images")

        loaded_images = 0
        failed_images = 0
        for img in all_images:
            natural_width = driver.execute_script("return arguments[0].naturalWidth;", img)
            if natural_width and natural_width > 0:
                loaded_images += 1
            else:
                failed_images += 1
        helper.test_result("Images loaded successfully", failed_images == 0, f"{loaded_images}/{len(all_images)} loaded")

        images_with_alt = sum(1 for img in all_images if img.get_attribute("alt"))
        helper.test_result("Images have alt text", images_with_alt == len(all_images), f"{images_with_alt} have alt")

        product_images = driver.find_elements(By.CSS_SELECTOR, "article img")
        helper.test_result("Product images present", len(product_images) >= 4, f"Found {len(product_images)} product images")
    except Exception as e:
        helper.test_result("Images & media tests", False, str(e))

    # === TEST 12: RESPONSIVE DESIGN ===
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
            helper.test_result(f"Responsive: {device_name}", product_section.is_displayed(), f"{width}x{height}")
            driver.save_screenshot(os.path.join(Config.SCREENSHOT_DIR, f"responsive_{width}x{height}.png"))
        except Exception as e:
            helper.test_result(f"Responsive: {device_name}", False, str(e))

    driver.maximize_window()
    time.sleep(1)

    # === TEST 13: INTERACTIVE ELEMENTS ===
    print("\n" + "=" * 80)
    print("TEST SUITE 13: INTERACTIVE ELEMENTS")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)

        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        helper.test_result("Buttons present", len(all_buttons) > 0, f"Found {len(all_buttons)} buttons")

        clickable_buttons = sum(1 for btn in all_buttons if btn.is_displayed() and btn.is_enabled())
        helper.test_result("Buttons are clickable", clickable_buttons > 0, f"{clickable_buttons} clickable")

        elements_with_hover = driver.find_elements(By.CSS_SELECTOR, "[class*='hover:']")
        helper.test_result("Hover effects defined", len(elements_with_hover) > 0, f"{len(elements_with_hover)} elements")

        try:
            product_section = driver.find_element(By.ID, "product")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_section)
            time.sleep(1)
            product_cards = driver.find_elements(By.TAG_NAME, "article")
            if product_cards:
                actions = ActionChains(driver)
                actions.move_to_element(product_cards[0]).perform()
                time.sleep(0.5)
                helper.test_result("Hover action works", True, "Hovered over first product card")
            else:
                helper.test_result("Hover action works", False, "No product cards found")
        except Exception:
            helper.test_result("Hover action works", False)

        try:
            sections = ["product", "mitra", "investasi", "contact"]
            for section_id in sections:
                section = driver.find_element(By.ID, section_id)
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", section
                )
                time.sleep(0.3)
            helper.test_result("Smooth scroll works", True, f"Scrolled to {len(sections)} sections")
        except Exception:
            helper.test_result("Smooth scroll works", False)
    except Exception as e:
        helper.test_result("Interactive elements tests", False, str(e))

    # === TEST 14: SEO & ACCESSIBILITY ===
    print("\n" + "=" * 80)
    print("TEST SUITE 14: SEO & ACCESSIBILITY")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)

        try:
            meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
            desc_content = meta_desc.get_attribute("content")
            helper.test_result("Meta description exists", bool(desc_content), f"Length: {len(desc_content)}")
        except Exception:
            helper.test_result("Meta description exists", False)

        try:
            og_tags = driver.find_elements(By.CSS_SELECTOR, "meta[property^='og:']")
            helper.test_result("Open Graph tags present", len(og_tags) > 0, f"{len(og_tags)} OG tags")
        except Exception:
            helper.test_result("Open Graph tags present", False)

        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        helper.test_result("H1 tag present", len(h1_tags) >= 1, f"{len(h1_tags)} H1")
        helper.test_result("Only one H1 tag", len(h1_tags) == 1, "SEO best practice")

        h2_tags = driver.find_elements(By.TAG_NAME, "h2")
        helper.test_result("H2 tags present", len(h2_tags) > 0, f"{len(h2_tags)} H2")

        h3_tags = driver.find_elements(By.TAG_NAME, "h3")
        helper.test_result("H3 tags present", len(h3_tags) > 0, f"{len(h3_tags)} H3")

        html_tag = driver.find_element(By.TAG_NAME, "html")
        lang = html_tag.get_attribute("lang")
        helper.test_result("Language attribute set", lang is not None, f"Language: {lang}")

        try:
            viewport = driver.find_element(By.CSS_SELECTOR, "meta[name='viewport']")
            helper.test_result("Viewport meta tag exists", True)
        except Exception:
            helper.test_result("Viewport meta tag exists", False)

        try:
            favicon = driver.find_element(By.CSS_SELECTOR, "link[rel*='icon']")
            helper.test_result("Favicon exists", True)
        except Exception:
            helper.test_result("Favicon exists", False)
    except Exception as e:
        helper.test_result("SEO & accessibility tests", False, str(e))

    # === TEST 15: PERFORMANCE ===
    print("\n" + "=" * 80)
    print("TEST SUITE 15: PERFORMANCE")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        base.wait_for_ready()

        dom_content_loaded = driver.execute_script(
            "return window.performance.timing.domContentLoadedEventEnd - "
            "window.performance.timing.navigationStart"
        )
        helper.test_result("DOM content loaded time < 3000ms", dom_content_loaded < 3000, f"{dom_content_loaded} ms")

        total_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd - "
            "window.performance.timing.navigationStart"
        )
        helper.test_result("Total page load time < 5000ms", total_load_time < 5000, f"{total_load_time} ms")

        resources = driver.execute_script("return window.performance.getEntriesByType('resource').length")
        helper.test_result("Resource count reasonable (<200)", resources < 200, f"{resources} resources")

        page_size = len(driver.page_source)
        helper.test_result("Page size reasonable (<500kB)", page_size < 500000, f"{page_size} bytes")
    except Exception as e:
        helper.test_result("Performance tests", False, str(e))

    # === TEST 16: BUSINESS CRITICAL DATA ===
    print("\n" + "=" * 80)
    print("TEST SUITE 16: BUSINESS CRITICAL DATA")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)
        page_content = driver.page_source.lower()

        helper.test_result(
            "Buyback price Rp 15.000/kg", "15.000" in driver.page_source or "15000" in driver.page_source
        )
        helper.test_result("ROI 12% mentioned", "12" in driver.page_source and "%" in driver.page_source)
        helper.test_result("Phone +62 811-359-0718", "811" in driver.page_source and "359" in driver.page_source)
        helper.test_result("Email info@dhisnivara.id", "info@dhisnivara.id" in page_content)
        helper.test_result("Location: Malang, Jawa Timur", "malang" in page_content and "jawa timur" in page_content)
        helper.test_result("IoT Temperature 24°C", "24" in driver.page_source)
        helper.test_result("IoT Humidity 85%", "85%" in driver.page_source)

        product_names = ["Tiram Putih", "Tiram Coklat", "Kuping", "Shiitake"]
        for product_name in product_names:
            helper.test_result(f"Product: {product_name}", product_name.lower() in page_content)
    except Exception as e:
        helper.test_result("Business critical data tests", False, str(e))

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
