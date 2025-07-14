from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging
import os

logger = logging.getLogger(__name__)

class MainPage:
    CONTRACT_NAME = (By.ID, "kz.halyk.onlinebank.stage:id/contract_name_text_view")
    ONLINE_DUKEN_BTN = (By.XPATH, '(//android.view.ViewGroup[@resource-id="kz.halyk.onlinebank.stage:id/container"])[1]')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_main_page(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, "kz.halyk.onlinebank.stage:id/contract_name_text_view"))
        )

    # def dismiss_hint(self):
    #     size = self.driver.get_window_size()
    #     x = size['width'] // 2
    #     y = int(size['height'] * 0.1)
    #     os.system(f"adb shell input tap {x} {y}")

    def dismiss_hint(self):
        size = self.driver.get_window_size()
        x = size['width'] // 2
        y = int(size['height'] * 0.1)
        try:
            hint = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, "id_подсказки_или_xpath"))
            )
            if hint.is_displayed():
                os.system(f"adb shell input tap {x} {y}")
                time.sleep(1)
        except TimeoutException:
            print("[INFO] Подсказка не найдена, тапать не будем.")

    def wait_until_loaded(self, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.CONTRACT_NAME)
        )

    def is_text_present(self, expected_text, timeout=10):
        self.wait_for_main_page(timeout=timeout)
        time.sleep(1)
        all_text_views = self.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
        for el in all_text_views:
            if expected_text in el.text.strip():
                print(f"[INFO] '{expected_text}' найден в '{el.text.strip()}'")
                return True
        print(f"[WARNING] '{expected_text}' не найден ни в одном элементе.")
        return False

    def select_company_by_name(self, name):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTRACT_NAME)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CONTRACT_NAME)
        )
        if self.is_text_present(name):
            elems = self.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
            for el in elems:
                if name in el.text.strip():
                    el.click()
                    return True
        return False

    def go_to_online_duken(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ONLINE_DUKEN_BTN)
        )
        btn.click()

    def is_marketplace_loaded(self, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@text="main logo"]'))
        )
