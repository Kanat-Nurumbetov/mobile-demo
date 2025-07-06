from appium import webdriver
from appium.options.android import UiAutomator2Options
import pytest

@pytest.fixture(scope='module')
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app = r"C:\Users\Kanat\AndroidStudioProjects\b2b\app\build\outputs\apk\debug\app-debug.apk"
    # можешь добавить ещё нужные опции

    driver = webdriver.Remote('http://localhost:4723', options=options)
    yield driver
    driver.quit()

def test_start_app(driver):
    assert driver is not None
