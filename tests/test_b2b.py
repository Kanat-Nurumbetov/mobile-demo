from pages.main_page_ob import MainPage
from pages.od_main_page import OdMainPage
from pages.qr_scaner_page import QrScanerPage
import time, pytest


def test_main_page_ob(driver, login):
    main = MainPage(driver)
    main.wait_for_main_page()
    main.dismiss_hint()
    time.sleep(2)
    driver.save_screenshot("screenshots/after_dismiss_1.png")
    main.dismiss_hint()
    time.sleep(2)
    driver.save_screenshot("screenshots/after_dismiss_2.png")

    assert main.is_text_present("name050201.442894"), "Ожидаемый текст не найден на главной!"

# def test_select_right_contract(driver, login):
#     main = MainPage(driver)
#     main.wait_for_main_page()
#
#     main.select_company_by_name("name140124.206282")
#     time.sleep(2)
#     driver.save_screenshot("screenshots/after_permission.png")
#     assert main.is_text_present("name140124.206282")

def test_go_to_online_duken(driver, login):
    main = MainPage(driver)
    main.go_to_online_duken()
    driver.save_screenshot("screenshots/after_od_enter.png")

    assert main.is_marketplace_loaded(), "Marketplace не загрузился"

@pytest.mark.parametrize(
    "qr_image",
    ["distrA", "distrB"],          # ключи из QR_PAYLOADS
    indirect=True,                 # передаём в фикстуру qr_image
    ids=["Distributor-A", "Distributor-B"]
)
def test_scan_and_pay(driver, qr_image):
    od = OdMainPage(driver)
    od.select_qr_scaner()
    driver.save_screenshot("screenshots/after_qr_selected.png")

    scanner = QrScanerPage(driver)
    scanner.qr_gallery_open(qr_image)
    driver.save_screenshot("screenshots/after_load_qr.png")