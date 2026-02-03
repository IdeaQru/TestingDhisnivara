from config.config import Config
from utils.driver_factory import DriverFactory
from pages.product_section import ProductSection

def test_product_section_basic():
    driver = DriverFactory.get_driver()
    driver.get(Config.BASE_URL)

    product = ProductSection(driver)
    product.scroll_to_section()

    assert product.is_fresh_tab_displayed()
    assert product.is_cooked_tab_displayed()

    # jumlah product
    assert product.get_product_count() >= 4

    # nama produk
    names = product.get_product_names()
    for expected in ["Jamur Tiram Putih", "Jamur Tiram Coklat", "Jamur Kuping", "Jamur Shiitake"]:
        assert any(expected in n for n in names)

    # gambar & tombol
    assert product.are_all_images_loaded()
    assert product.are_all_buttons_clickable()

    # CTA
    assert product.is_katalog_button_displayed()
    assert product.is_sales_button_displayed()

    driver.quit()
