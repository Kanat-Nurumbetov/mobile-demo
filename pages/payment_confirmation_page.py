from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time
import logging

logger = logging.getLogger(__name__)

class PaymentConfirmationPage(BasePage):
    # Локаторы страницы подтверждения
    CONFIRM_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/confirm_payment")
    CANCEL_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/cancel_payment")
    EDIT_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/edit_payment")

    # Информация о платеже
    PAYMENT_AMOUNT = (By.ID, "kz.halyk.onlinebank.stage:id/payment_amount")
    RECIPIENT_NAME = (By.ID, "kz.halyk.onlinebank.stage:id/recipient_name")
    PAYMENT_DETAILS = (By.ID, "kz.halyk.onlinebank.stage:id/payment_details")

    # Результат операции
    SUCCESS_MESSAGE = (By.ID, "kz.halyk.onlinebank.stage:id/success_message")
    ERROR_MESSAGE = (By.ID, "kz.halyk.onlinebank.stage:id/error_message")
    PROCESSING_INDICATOR = (By.ID, "kz.halyk.onlinebank.stage:id/processing")

    # Успешный результат
    SUCCESS_ICON = (By.ID, "kz.halyk.onlinebank.stage:id/success_icon")
    TRANSACTION_ID = (By.ID, "kz.halyk.onlinebank.stage:id/transaction_id")

    def wait_for_confirmation_page(self):
        """Ожидать загрузки страницы подтверждения"""
        logger.info("Ожидаем страницу подтверждения платежа...")
        self.find_element(self.CONFIRM_BUTTON)
        logger.info("Страница подтверждения загружена")

    def get_payment_info(self):
        """Получить информацию о платеже"""
        info = {}

        try:
            if self.is_element_present(self.PAYMENT_AMOUNT):
                info['amount'] = self.get_element_text(self.PAYMENT_AMOUNT)
        except:
            info['amount'] = None

        try:
            if self.is_element_present(self.RECIPIENT_NAME):
                info['recipient'] = self.get_element_text(self.RECIPIENT_NAME)
        except:
            info['recipient'] = None

        try:
            if self.is_element_present(self.PAYMENT_DETAILS):
                info['details'] = self.get_element_text(self.PAYMENT_DETAILS)
        except:
            info['details'] = None

        logger.info(f"Информация о платеже: {info}")
        return info

    def confirm_payment(self):
        """Подтвердить платеж"""
        try:
            logger.info("Подтверждаем платеж...")
            self.click_element(self.CONFIRM_BUTTON)
            time.sleep(3)  # Ждем обработки
            logger.info("Платеж подтвержден")
            return True
        except Exception as e:
            logger.error(f"Не удалось подтвердить платеж: {e}")
            return False

    def cancel_payment(self):
        """Отменить платеж"""
        try:
            logger.info("Отменяем платеж...")
            self.click_element(self.CANCEL_BUTTON)
            time.sleep(2)
            logger.info("Платеж отменен")
            return True
        except Exception as e:
            logger.error(f"Не удалось отменить платеж: {e}")
            return False

    def wait_for_payment_result(self, timeout=30):
        """Ожидать результата платежа"""
        logger.info("Ожидаем результата обработки платежа...")

        end_time = time.time() + timeout
        while time.time() < end_time:
            # Проверяем успешный результат
            if self.is_element_present(self.SUCCESS_MESSAGE, timeout=1) or \
                    self.is_element_present(self.SUCCESS_ICON, timeout=1):
                logger.info("Платеж выполнен успешно")
                return "success"

            # Проверяем ошибку
            if self.is_element_present(self.ERROR_MESSAGE, timeout=1):
                logger.info("Платеж завершился ошибкой")
                return "error"

            # Проверяем, что еще обрабатывается
            if self.is_element_present(self.PROCESSING_INDICATOR, timeout=1):
                logger.info("Платеж обрабатывается...")
                time.sleep(2)
                continue

            time.sleep(1)

        logger.warning("Истекло время ожидания результата платежа")
        return "timeout"

    def is_payment_successful(self):
        """Проверить успешность платежа"""
        return (self.is_element_present(self.SUCCESS_MESSAGE) or
                self.is_element_present(self.SUCCESS_ICON))

    def is_payment_failed(self):
        """Проверить неуспешность платежа"""
        return self.is_element_present(self.ERROR_MESSAGE)

    def get_error_message(self):
        """Получить текст ошибки"""
        try:
            if self.is_payment_failed():
                return self.get_element_text(self.ERROR_MESSAGE)
        except:
            pass
        return None

    def get_transaction_id(self):
        """Получить ID транзакции"""
        try:
            if self.is_element_present(self.TRANSACTION_ID):
                return self.get_element_text(self.TRANSACTION_ID)
        except:
            pass
        return None