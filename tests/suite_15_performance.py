# tests/suite_15_performance.py
from config.config import Config
from pages.base_page import BasePage

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 15: PERFORMANCE")
    print("=" * 80)
    try:
        base = BasePage(driver)
        driver.get(Config.BASE_URL)
        base.wait_for_ready()

        dom_content_loaded = driver.execute_script(
            "return window.performance.timing.domContentLoadedEventEnd - "
            "window.performance.timing.navigationStart"
        )
        helper.test_result(
            "DOM content loaded time < 3000ms",
            dom_content_loaded < 3000,
            f"{dom_content_loaded} ms",
        )

        total_load_time = driver.execute_script(
            "return window.performance.timing.loadEventEnd - "
            "window.performance.timing.navigationStart"
        )
        helper.test_result(
            "Total page load time < 5000ms",
            total_load_time < 5000,
            f"{total_load_time} ms",
        )

        resources = driver.execute_script(
            "return window.performance.getEntriesByType('resource').length"
        )
        helper.test_result(
            "Resource count reasonable (<200)",
            resources < 200,
            f"{resources} resources",
        )

        page_size = len(driver.page_source)
        helper.test_result(
            "Page size reasonable (<500kB)",
            page_size < 500000,
            f"{page_size} bytes",
        )

    except Exception as e:
        helper.test_result("Performance tests", False, str(e))
