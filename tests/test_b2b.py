from pages.main_page_ob import MainPage
import time


def test_main_page_ob(driver, login):
    main = MainPage(driver)
    main.wait_for_main_page()
    main.dismiss_hint()
    time.sleep(2)
    driver.save_screenshot("screenshots/after_dismiss_1.png")
    main.dismiss_hint()
    time.sleep(2)
    driver.save_screenshot("screenshots/after_dismiss_2.png")

    assert main.is_text_present("name050201.322318"), "Ожидаемый текст не найден на главной!"

def test_select_right_contract(driver, login):
    main = MainPage(driver)
    main.wait_for_main_page()

    main.select_company_by_name("name140124.206282")
    time.sleep(2)
    driver.save_screenshot("screenshots/after_permission.png")
    assert main.is_text_present("name140124.206282")

def test_go_to_online_duken(driver, login):
    main = MainPage(driver)
    main.go_to_online_duken()

    assert main.is_marketplace_loaded(), "Marketplace не загрузился"