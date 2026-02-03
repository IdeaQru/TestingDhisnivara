# tests/suite_06_lokasi.py

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 6: LOKASI KUMBUNG")
    print("=" * 80)
    try:
        page_text = driver.page_source

        locations = ["Puncu", "Kediri", "Harjo Kuncaran", "Malang", "Sumbermanjing"]
        for location in locations:
            helper.test_result(
                f"Location mentioned: {location}",
                location in page_text,
            )

        helper.test_result(
            "RT/RW information present",
            ("RT" in page_text and "RW" in page_text)
            or "RT 04" in page_text
            or "RT 06" in page_text,
        )

    except Exception as e:
        helper.test_result("Lokasi kumbung tests", False, str(e))
