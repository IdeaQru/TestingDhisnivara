
from selenium.webdriver.common.by import By

def run_suite(driver, helper):
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
