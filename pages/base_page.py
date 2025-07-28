from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """Базовый класс для всех Page Object классов"""

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, timeout)

    def find_element(self, locator):
        """Найти элемент с ожиданием"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Элемент не найден: {locator}")
            raise

    def find_clickable_element(self, locator):
        """Найти кликабельный элемент с ожиданием"""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.error(f"Кликабельный элемент не найден: {locator}")
            raise

    def click_element(self, locator):
        """Кликнуть по элементу"""
        element = self.find_clickable_element(locator)
        element.click()
        logger.info(f"Клик по элементу: {locator}")

    def enter_text(self, locator, text):
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Введен текст '{text}' в поле: {locator}")

    def is_element_present(self, locator, timeout=5):
        """Проверить наличие элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_element_text(self, locator):
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text

    def take_screenshot(self, name):
        """Сделать скриншот"""
        import os
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{name}.png"
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Скриншот сохранен: {screenshot_path}")
        return screenshot_path