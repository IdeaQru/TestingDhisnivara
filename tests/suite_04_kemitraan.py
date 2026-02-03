
from selenium.webdriver.common.by import By
from pages.kemitraan_section import KemitraanSection

def run_suite(driver, helper):
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
