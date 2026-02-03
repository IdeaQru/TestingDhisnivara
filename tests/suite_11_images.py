# tests/suite_11_images.py
from selenium.webdriver.common.by import By

def run_suite(driver, helper):
    print("\n" + "=" * 80)
    print("TEST SUITE 11: IMAGES & MEDIA")
    print("=" * 80)
    try:
        all_images = driver.find_elements(By.TAG_NAME, "img")
        helper.test_result(
            "Images present on page",
            len(all_images) > 0,
            f"Found {len(all_images)} images",
        )

        loaded_images = 0
        failed_images = 0
        for img in all_images:
            natural_width = driver.execute_script(
                "return arguments[0].naturalWidth;", img
            )
            if natural_width and natural_width > 0:
                loaded_images += 1
            else:
                failed_images += 1

        helper.test_result(
            "Images loaded successfully",
            failed_images == 0,
            f"{loaded_images}/{len(all_images)} loaded",
        )

        images_with_alt = sum(
            1 for img in all_images if img.get_attribute("alt")
        )
        helper.test_result(
            "Images have alt text",
            images_with_alt == len(all_images),
            f"{images_with_alt}/{len(all_images)} have alt",
        )

        product_images = driver.find_elements(
            By.CSS_SELECTOR, "article img"
        )
        helper.test_result(
            "Product images present",
            len(product_images) >= 4,
            f"Found {len(product_images)} product images",
        )

    except Exception as e:
        helper.test_result("Images & media tests", False, str(e))
