# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ========== NAVIGATION ==========
    def open(self, url: str):
        """Open URL dan return self (untuk chaining)."""
        self.driver.get(url)
        return self

    def wait_for_ready(self, timeout=None):
        """Wait sampai document.readyState == 'complete'."""
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        w.until(lambda d: d.execute_script("return document.readyState") == "complete")
        return self

    # ========== LOCATOR HELPERS ==========
    def find_element(self, locator):
        by, value = locator
        return self.driver.find_element(by, value)

    def find_elements(self, locator):
        by, value = locator
        return self.driver.find_elements(by, value)

    def wait_for_visible(self, locator, timeout=None):
        by, value = locator
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.visibility_of_element_located((by, value)))

    def wait_for_clickable(self, locator, timeout=None):
        by, value = locator
        w = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return w.until(EC.element_to_be_clickable((by, value)))

    # ========== ACTIONS ==========
    def click(self, locator):
        el = self.wait_for_clickable(locator)
        el.click()
        return el

    def click_js(self, locator):
        el = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].click();", el)
        return el

    def get_text(self, locator):
        el = self.wait_for_visible(locator)
        return el.text

    def is_displayed(self, locator):
        try:
            el = self.find_element(locator)
            return el.is_displayed()
        except Exception:
            return False

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    # ========== SCROLL HELPERS ==========
    def scroll_into_view(self, locator_or_element, block="center"):
        if isinstance(locator_or_element, tuple):
            el = self.find_element(locator_or_element)
        else:
            el = locator_or_element
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: arguments[1]});",
            el,
            block,
        )
        return el

    def scroll_to_section(self, section_id: str, block="center"):
        el = self.driver.find_element(By.ID, section_id)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: arguments[1]});",
            el,
            block,
        )
        return el
