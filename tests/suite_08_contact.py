# tests/suite_08_contact.py
from selenium.webdriver.common.by import By
from config.config import Config
from pages.contact_section import ContactSection

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 8: CONTACT SECTION")
    print("=" * 80)
    try:
        contact = ContactSection(driver)
        section = contact.get_section()

        # Heading
        try:
            h2 = section.find_element(By.TAG_NAME, "h2")
            helper.test_result(
                "Contact section has heading",
                h2.is_displayed(),
            )
        except Exception:
            helper.test_result("Contact section has heading", False)

        txt = contact.text()
        src = contact.page_source()

        helper.test_result(
            "Phone number present",
            Config.PHONE_NUMBER in src or "811-359-0718" in src,
        )

        helper.test_result(
            "Email address present",
            Config.EMAIL in src or "@dhisnivara" in src,
        )

        helper.test_result(
            "Physical address present",
            "Malang" in txt and "Jawa Timur" in txt,
        )

        helper.test_result(
            "Postal code present",
            "65176" in txt,
        )

        helper.take_screenshot("08_contact_section.png")

    except Exception as e:
        helper.test_result("Contact section tests", False, str(e))
