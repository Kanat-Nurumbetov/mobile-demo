import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope='session')
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = "kz.halyk.onlinebank.stage"
    options.app_activity = "kz.halyk.onlinebank.ui_release4.screens.splash.SplashActivity"
    # options.app = r"C:\Users\Kanat\AndroidStudioProjects\b2b\app\build\outputs\apk\debug\app-debug.apk"
    options.app = r"/Users/a00059362/AndroidStudioProjects/mobiledemo/app/build/intermediates/apk/debug/app-stage-debug.apk"
    options.automation_name = "UiAutomator2"
    options.auto_grant_permissions = True
    options.app_wait_activity = "*"

    driver = webdriver.Remote('http://localhost:4723', options=options)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_exception_interact(node, call, report):
    # Проверяем, что это действительно функция с фикстурами
    driver = getattr(node, "funcargs", {}).get("driver", None)
    if driver:
        import os
        os.makedirs("screenshots", exist_ok=True)
        screenshot_name = f"screenshots/{node.name}_failed.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n[Screenshot saved]: {screenshot_name}")
    yield
