# pages/kemitraan_section.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class KemitraanSection(BasePage):
    SECTION_ID = "mitra"

    FEATURES = [
        "Desain & Konstruksi",
        "Supply Baglog",
        "Guaranteed Buyback",
        "IoT Monitoring",
        "15.000",
    ]

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_section(self):
        section = self.driver.find_element(By.ID, self.SECTION_ID)
        self.scroll_into_view(section, block="center")
        return section

    def text(self):
        return self.get_section().text

    def has_all_features(self):
        t = self.text()
        return {f: (f in t) for f in self.FEATURES}
