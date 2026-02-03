# pages/investasi_section.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class InvestasiSection(BasePage):
    SECTION_ID = "investasi"

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_section(self):
        section = self.driver.find_element(By.ID, self.SECTION_ID)
        self.scroll_into_view(section, block="center")
        return section

    def get_tables(self):
        return self.get_section().find_elements(By.TAG_NAME, "table")

    def get_text(self):
        return self.get_section().text
