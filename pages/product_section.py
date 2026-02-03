# pages/product_section.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductSection(BasePage):
    # Locators
    SECTION_ID = (By.ID, "product")
    HEADING = (By.CSS_SELECTOR, "#product h2")
    DESCRIPTION = (By.CSS_SELECTOR, "#product p")
    FRESH_TAB = (By.XPATH, "//button[contains(text(), 'Jamur Segar')]")
    COOKED_TAB = (By.XPATH, "//button[contains(text(), 'Produk Olahan')]")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "#product article")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "#product article h3")
    PRODUCT_BADGES = (By.CSS_SELECTOR, "#product article span[class*='bg-white']")
    PRODUCT_DESCRIPTIONS = (By.CSS_SELECTOR, "#product article p")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, "#product article img")
    PRODUCT_BUTTONS = (By.CSS_SELECTOR, "#product article button")
    KATALOG_BUTTON = (By.LINK_TEXT, "Lihat Katalog Lengkap")
    SALES_BUTTON = (By.PARTIAL_LINK_TEXT, "Hubungi Sales")

    # === INI YANG BELUM ADA ===
    def get_section(self):
        """Return WebElement untuk section product + scroll ke view."""
        section = self.find_element(self.SECTION_ID)
        self.scroll_into_view(section, block="center")
        return section

    def scroll_to_section(self):
        """Alias: scroll saja, lalu return self."""
        self.scroll_into_view(self.SECTION_ID, block="center")
        return self

    def get_product_cards(self):
        return self.find_elements(self.PRODUCT_CARDS)

    def get_product_names(self):
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [e.text for e in elements]

    def get_badges_count(self):
        badges = self.find_elements(self.PRODUCT_BADGES)
        return len([b for b in badges if b.text])

    def get_descriptions_count(self, min_len=20):
        descs = self.find_elements(self.PRODUCT_DESCRIPTIONS)
        return len([d for d in descs if len(d.text) >= min_len])

    def get_loaded_images_count(self):
        imgs = self.find_elements(self.PRODUCT_IMAGES)
        count = 0
        for img in imgs:
            w = self.execute_script("return arguments[0].naturalWidth;", img)
            if w and w > 0:
                count += 1
        return count

    def click_fresh_tab(self):
        self.click_js(self.FRESH_TAB)
        return self

    def click_cooked_tab(self):
        self.click_js(self.COOKED_TAB)
        return self
