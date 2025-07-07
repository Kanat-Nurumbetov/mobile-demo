from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging
import os

logger = logging.getLogger(__name__)

class MainPage:
    CONTRACT_NAME = (By.ID, "kz.halyk.onlinebank.stage:id/contract_name_text_view")
    MENU_MORE = (By.ID, "kz.halyk.onlinebank.stage:id/navigation_more")
    USER_NAME = (By.ID, "kz.halyk.onlinebank.stage:id/tv_name")
    ONLINE_DUKEN_BTN = (By.XPATH, '//*[@text="OnlineDuken"]')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_main_page(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.ID, "kz.halyk.onlinebank.stage:id/contract_name_text_view"))
        )

    def dismiss_hint(self):
        size = self.driver.get_window_size()
        x = size['width'] // 2
        y = int(size['height'] * 0.1)
        os.system(f"adb shell input tap {x} {y}")

    def wait_until_loaded(self, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.CONTRACT_NAME)
        )

    def get_contract_name(self):
        return self.wait_until_loaded().text.strip()

    def is_text_present(self, expected_text, timeout=10):
        self.wait_until_loaded(timeout=timeout)
        time.sleep(1)
        all_text_views = self.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
        for el in all_text_views:
            if expected_text in el.text.strip():
                print(f"[INFO] '{expected_text}' найден в '{el.text.strip()}'")
                return True
        print(f"[WARNING] '{expected_text}' не найден ни в одном элементе.")
        return False

    def get_contract_name(self):
        return self.wait_until_loaded().text.strip()

    def open_menu_more(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MENU_MORE)
        ).click()

    def select_company_by_name(self, name):
        # Открыть выбор компании
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.USER_NAME)
        ).click()
        # Клик по нужной компании (по тексту)
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@text="{name}"]'))
        )
        elem.click()

    def go_to_online_duken(self):
        # Ждем появления кнопки OnlineDuken и кликаем по ней
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ONLINE_DUKEN_BTN)
        )
        btn.click()

    def is_marketplace_loaded(self, timeout=15):
        # Проверяем наличие лого/текста маркета
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@text="main logo"]'))
        )
