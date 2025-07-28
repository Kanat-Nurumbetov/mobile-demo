from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    # Локаторы
    PHONE_INPUT = (By.ID, "kz.halyk.onlinebank.stage:id/phone_input")
    LOGIN_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/login_button")
    ERROR_MESSAGE = (By.ID, "kz.halyk.onlinebank.stage:id/error_message")

    def enter_phone(self, phone):
        """Ввести номер телефона"""
        self.enter_text(self.PHONE_INPUT, phone)
        time.sleep(1)  # Небольшая пауза для UI

    def click_login(self):
        """Нажать кнопку входа"""
        self.click_element(self.LOGIN_BUTTON)
        time.sleep(2)  # Ждем переход на следующую страницу

    def is_error_displayed(self):
        """Проверить наличие ошибки"""
        return self.is_element_present(self.ERROR_MESSAGE)

    def get_error_text(self):
        """Получить текст ошибки"""
        if self.is_error_displayed():
            return self.get_element_text(self.ERROR_MESSAGE)
        return None