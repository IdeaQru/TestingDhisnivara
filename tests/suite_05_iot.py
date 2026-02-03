# tests/suite_05_iot.py

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 5: IoT MONITORING")
    print("=" * 80)
    try:
        page_source = driver.page_source

        helper.test_result(
            "Temperature data present",
            "24°C" in page_source or "24°" in page_source,
        )

        helper.test_result(
            "Humidity data present",
            "85%" in page_source,
        )

        helper.test_result(
            "System status present",
            "98%" in page_source or "OK" in page_source,
        )

        iot_keywords = ["Real-time", "Monitoring", "Temperature", "Humidity", "System"]
        for keyword in iot_keywords:
            helper.test_result(
                f"IoT keyword: {keyword}",
                keyword in page_source,
            )

    except Exception as e:
        helper.test_result("IoT monitoring tests", False, str(e))
