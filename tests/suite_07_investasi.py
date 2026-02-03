# tests/suite_07_investasi.py
from selenium.webdriver.common.by import By
from pages.investasi_section import InvestasiSection

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 7: INVESTASI SECTION")
    print("=" * 80)
    try:
        inv = InvestasiSection(driver)
        section = inv.get_section()

        # Heading
        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result(
                "Investasi section has heading",
                h2.is_displayed(),
            )
        except Exception:
            helper.test_result("Investasi section has heading", False)

        # Tabel investasi
        tables = inv.get_tables()
        helper.test_result(
            "Investment table exists",
            len(tables) > 0,
            f"{len(tables)} table(s)",
        )

        text = inv.get_text()
        helper.test_result(
            "ROI % mentioned",
            "12" in text and "%" in text,
        )

        # Kata kunci investasi
        investment_keywords = ["Modal", "Return", "Tenor", "Investasi", "Keuntungan"]
        for keyword in investment_keywords:
            helper.test_result(
                f"Investment keyword: {keyword}",
                keyword in text,
            )

        helper.take_screenshot("07_investasi_section.png")

    except Exception as e:
        helper.test_result("Investasi section tests", False, str(e))
