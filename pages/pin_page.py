from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
import logging

logger = logging.getLogger(__name__)

class PinPage(BasePage):
    # Локаторы для цифр PIN-кода
    PIN_DIGIT = "//android.widget.TextView[@text='{}']"
    BACKSPACE_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/backspace")
    ERROR_MESSAGE = (By.ID, "kz.halyk.onlinebank.stage:id/pin_error")
    PIN_DOTS = (By.ID, "kz.halyk.onlinebank.stage:id/pin_dots")

    def wait_for_pin_screen(self):
        """Ожидать появления экрана PIN"""
        logger.info("Ожидаем экран ввода PIN...")
        # Ждем появления цифры "0" как индикатор загрузки PIN экрана
        self.find_element((By.XPATH, self.PIN_DIGIT.format("0")))
        logger.info("Экран PIN загружен")

    def enter_pin(self, pin: str):
        """Ввести PIN код"""
        logger.info(f"Вводим PIN: {'*' * len(pin)}")

        for i, digit in enumerate(pin):
            try:
                digit_locator = (By.XPATH, self.PIN_DIGIT.format(digit))
                self.click_element(digit_locator)
                time.sleep(0.5)  # Пауза между нажатиями
                logger.info(f"Введена {i+1}-я цифра PIN")
            except Exception as e:
                logger.error(f"Ошибка при вводе цифры {digit}: {e}")
                self.take_screenshot(f"pin_error_digit_{digit}")
                raise

        # После ввода PIN может быть автоматический переход
        time.sleep(2)

    def clear_pin(self):
        """Очистить введенный PIN"""
        for _ in range(4):  # Максимум 4 цифры
            if self.is_element_present(self.BACKSPACE_BUTTON):
                self.click_element(self.BACKSPACE_BUTTON)
                time.sleep(0.3)

    def is_pin_error_displayed(self):
        """Проверить ошибку PIN"""
        return self.is_element_present(self.ERROR_MESSAGE)

    def get_pin_error_text(self):
        """Получить текст ошибки PIN"""
        if self.is_pin_error_displayed():
            return self.get_element_text(self.ERROR_MESSAGE)
        return None