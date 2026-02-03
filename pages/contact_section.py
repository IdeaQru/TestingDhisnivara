# pages/contact_section.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class ContactSection(BasePage):
    SECTION_ID = "contact"

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_section(self):
        section = self.driver.find_element(By.ID, self.SECTION_ID)
        self.scroll_into_view(section, block="center")
        return section

    def text(self):
        return self.get_section().text

    def page_source(self):
        return self.driver.page_source
