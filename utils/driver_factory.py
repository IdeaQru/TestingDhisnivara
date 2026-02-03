"""
WebDriver Factory - Setup dan konfigurasi driver
"""
import sys
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config

# Fix encoding untuk Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class DriverFactory:
    @staticmethod
    def get_driver(browser=None):
        """
        Create and return WebDriver instance
        
        Args:
            browser (str): Browser type (chrome, firefox, edge)
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser or Config.BROWSER
        
        if browser.lower() == "chrome":
            return DriverFactory._get_chrome_driver()
        elif browser.lower() == "firefox":
            return DriverFactory._get_firefox_driver()
        else:
            raise ValueError(f"Browser '{browser}' not supported")
    
    @staticmethod
    def _get_chrome_driver():
        """Chrome driver with options"""
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        
        if Config.HEADLESS:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        
        if Config.MAXIMIZE_WINDOW:
            chrome_options.add_argument("--start-maximized")
        
        # Additional options untuk stabilitas
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _get_firefox_driver():
        """Firefox driver with options"""
        firefox_options = FirefoxOptions()
        
        if Config.HEADLESS:
            firefox_options.add_argument("--headless")
        
        driver = webdriver.Firefox(options=firefox_options)
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
        if Config.MAXIMIZE_WINDOW:
            driver.maximize_window()
        
        return driver
    
    @staticmethod
    def get_wait(driver, timeout=None):
        """
        Get WebDriverWait instance
        
        Args:
            driver: WebDriver instance
            timeout (int): Wait timeout in seconds
            
        Returns:
            WebDriverWait: Wait instance
        """
        timeout = timeout or Config.EXPLICIT_WAIT
        return WebDriverWait(driver, timeout)
