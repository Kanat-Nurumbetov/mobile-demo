import pytest, os
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.login_page import LoginPage
from pages.otp_page import OtpPage
from pages.permissions_page import PermissionsPage
from pages.pin_page import PinPage
from pages.od_main_page import OdMainPage
from utils.qr_generator import make_qr
from data.qr_payloads import QR_PAYLOADS


@pytest.fixture(scope='session')
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "kz.halyk.onlinebank.stage"
    options.app_activity = "kz.halyk.onlinebank.ui_release4.screens.splash.SplashActivity"
    # options.app = r"C:\Users\Kanat\AndroidStudioProjects\b2b\app\build\outputs\apk\debug\app-debug.apk"
    # options.app = r"/Users/a00059362/AndroidStudioProjects/mobiledemo/app.apk"
    options.automation_name = "UiAutomator2"
    options.auto_grant_permissions = True
    options.adb_exec_timeout = 60000  # 60 секунд (в миллисекундах)
    options.uiautomator2_server_launch_timeout = 60000  # 60 секунд
    # options.app_wait_activity = "*"

    driver = webdriver.Remote('http://localhost:4723', options=options)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_exception_interact(node, call, report):
    driver = getattr(node, "funcargs", {}).get("driver", None)
    if driver:
        import os
        os.makedirs("screenshots", exist_ok=True)
        screenshot_name = f"screenshots/{node.name}_failed.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n[Screenshot saved]: {screenshot_name}")
    yield

@pytest.fixture(scope='session')
def login(driver):
        driver.save_screenshot("screenshots/before_any_actions.png")
        login = LoginPage(driver)
        login.enter_phone("7771112222")
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

@pytest.fixture
def qr_image(request, tmp_path, driver):

    distr = request.param
    payload_info = QR_PAYLOADS[distr]

    # локальный PNG
    local_file: Path = tmp_path / payload_info["file_name"]
    make_qr(payload_info["text"], local_file)

    # путь на эмуляторе
    device_file = f"/sdcard/Download/{payload_info['file_name']}"
    os.system(f"adb push {local_file} {device_file}")

    return device_file