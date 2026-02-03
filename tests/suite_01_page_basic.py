from config.config import Config

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 1: PAGE LOAD & BASIC INFORMATION")
    print("=" * 80)
    try:
        current_url = driver.current_url
        helper.test_result("Page loads successfully", Config.BASE_URL in current_url, f"URL: {current_url}")

        title = driver.title
        helper.test_result("Page has title", "Dhisnivara" in title, f"Title: {title}")

        nav_start = driver.execute_script("return window.performance.timing.navigationStart")
        load_end = driver.execute_script("return window.performance.timing.loadEventEnd")
        if load_end > 0:
            load_time = (load_end - nav_start) / 1000
            helper.test_result("Page load time < 5s", load_time < 5, f"{load_time:.2f} seconds")

        ready_state = driver.execute_script("return document.readyState")
        helper.test_result("Page ready state complete", ready_state == "complete", f"State: {ready_state}")
    except Exception as e:
        helper.test_result("Page load & basic info", False, str(e))
