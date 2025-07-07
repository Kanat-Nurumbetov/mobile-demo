from pages.login_page import LoginPage
from pages.otp_page import OtpPage
from pages.pin_page import PinPage
from pages.permissions_page import PermissionsPage
from pages.main_page_ob import MainPage
import time

def test_login(driver):
    driver.save_screenshot("screenshots/before_any_actions.png")
    login = LoginPage(driver)
    login.enter_phone("7073502010")
    driver.save_screenshot("screenshots/after_phone.png")
    login.click_login()
    driver.save_screenshot("screenshots/after_click.png")

    otp = OtpPage(driver)
    otp.enter_otp("000000")
    driver.save_screenshot("screenshots/after_otp.png")

    pin = PinPage(driver)
    pin.enter_pin("0000")
    driver.save_screenshot("screenshots/after_pin.png")
    pin.enter_pin("0000")
    driver.save_screenshot("screenshots/after_pin2.png")

    permissions = PermissionsPage(driver)
    permissions.click_next()
    driver.save_screenshot("screenshots/after_permission.png")

    main = MainPage(driver)
    main.dismiss_hint()
    driver.save_screenshot("screenshots/after_dismiss_1.png")# Закроет первую подсказку, если есть
    main.wait_for_main_page()
    main.dismiss_hint()
    driver.save_screenshot("screenshots/after_dismiss_2.png")

    assert main.is_text_present("name050201.322318"), "Ожидаемый текст не найден на главной!"# Закроет вторую подсказку, если есть

    actual_name = main.get_contract_name()
    assert actual_name == "name050201.322318", f"Наименование договора некорректно: {actual_name}"

def test_marketplace_access(driver):
    main = MainPage(driver)
    main.wait_until_loaded()
    main.dismiss_hint()  # если всплывашка есть

    # Перейти в меню "Еще"
    main.open_menu_more()

    # Сменить компанию (пример с name из твоего скрина)
    main.select_company_by_name("name140124.206282")
    time.sleep(2)  # иногда после смены нужна небольшая пауза

    # Кнопка OnlineDuken появляется сразу, кликнуть по ней
    main.go_to_online_duken()

    # Проверить, что маркетплейс открылся (есть main logo)
    assert main.is_marketplace_loaded(), "Marketplace не загрузился"