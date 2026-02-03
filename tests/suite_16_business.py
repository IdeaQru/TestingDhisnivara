# tests/suite_16_business.py
import time
from config.config import Config

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 16: BUSINESS CRITICAL DATA")
    print("=" * 80)
    try:
        driver.get(Config.BASE_URL)
        time.sleep(2)
        page_content = driver.page_source.lower()

        helper.test_result(
            "Buyback price Rp 15.000/kg",
            "15.000" in driver.page_source or "15000" in driver.page_source,
        )

        helper.test_result(
            "ROI 12% mentioned",
            "12" in driver.page_source and "%" in driver.page_source,
        )

        helper.test_result(
            "Phone +62 811-359-0718",
            "811" in driver.page_source and "359" in driver.page_source,
        )

        helper.test_result(
            "Email info@dhisnivara.id",
            "info@dhisnivara.id" in page_content,
        )

        helper.test_result(
            "Location: Malang, Jawa Timur",
            "malang" in page_content and "jawa timur" in page_content,
        )

        helper.test_result(
            "IoT Temperature 24°C",
            "24" in driver.page_source,
        )
        helper.test_result(
            "IoT Humidity 85%",
            "85%" in driver.page_source,
        )

        product_names = ["Tiram Putih", "Tiram Coklat", "Kuping", "Shiitake"]
        for product_name in product_names:
            helper.test_result(
                f"Product: {product_name}",
                product_name.lower() in page_content,
            )

    except Exception as e:
        helper.test_result("Business critical data tests", False, str(e))
