"""
Configuration file untuk test suite
"""

class Config:
    # Base URL
    BASE_URL = "https://dhisnivara.id"
    
    # Timeouts
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    # Browser settings
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    MAXIMIZE_WINDOW = True
    
    # Screenshot settings
    SCREENSHOT_DIR = "reports/screenshots"
    TAKE_SCREENSHOT_ON_FAILURE = True
    
    # Test data
    EXPECTED_PRODUCTS = [
        "Jamur Tiram Putih",
        "Jamur Tiram Coklat",
        "Jamur Kuping",
        "Jamur Shiitake"
    ]
    
    EXPECTED_LOCATIONS = [
        "Puncu",
        "Kediri",
        "Harjo Kuncaran",
        "Malang",
        "Sumbermanjing"
    ]
    
    # Contact info
    PHONE_NUMBER = "+62 811-359-0718"
    EMAIL = "info@dhisnivara.id"
    WHATSAPP_NUMBER = "628113590718"
    
    # Viewport sizes for responsive testing
    VIEWPORT_SIZES = [
        (375, 667, "Mobile (iPhone SE)"),
        (414, 896, "Mobile (iPhone XR)"),
        (768, 1024, "Tablet (iPad)"),
        (1024, 768, "Tablet Landscape"),
        (1366, 768, "Desktop (Laptop)"),
        (1920, 1080, "Desktop (Full HD)")
    ]
