from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time
import logging

logger = logging.getLogger(__name__)


class QrScanerPage(BasePage):
    # Локаторы QR сканера
    GALLERY_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/gallery")
    CAMERA_PERMISSION = (By.ID, "com.android.permissioncontroller:id/permission_allow_button")
    QR_FRAME = (By.ID, "kz.halyk.onlinebank.stage:id/qr_frame")
    FLASH_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/flash")

    # Локаторы галереи
    GALLERY_FIRST_IMAGE = (By.XPATH, "//android.widget.ImageView[1]")
    GALLERY_IMAGES = (By.XPATH, "//android.widget.ImageView")

    # Результат сканирования
    PAYMENT_FORM = (By.ID, "kz.halyk.onlinebank.stage:id/payment_form")
    AMOUNT_FIELD = (By.ID, "kz.halyk.onlinebank.stage:id/amount")
    RECIPIENT_FIELD = (By.ID, "kz.halyk.onlinebank.stage:id/recipient")
    PAY_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/pay_button")
    CANCEL_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/cancel_button")

    def wait_for_qr_scanner(self):
        """Ожидать загрузки QR сканера"""
        logger.info("Ожидаем загрузки QR сканера...")
        self.find_element(self.QR_FRAME)
        logger.info("QR сканер загружен")

    def allow_camera_permission(self):
        """Разрешить доступ к камере"""
        try:
            if self.is_element_present(self.CAMERA_PERMISSION, timeout=5):
                self.click_element(self.CAMERA_PERMISSION)
                logger.info("Разрешен доступ к камере")
                time.sleep(2)
        except TimeoutException:
            logger.info("Разрешение камеры не требуется")

    def open_gallery(self):
        """Открыть галерею для выбора QR изображения"""
        logger.info("Открываем галерею...")
        self.click_element(self.GALLERY_BUTTON)
        time.sleep(3)  # Ждем загрузки галереи
        logger.info("Галерея открыта")

    def select_qr_from_gallery(self, image_path: str = None):
        """Выбрать QR изображение из галереи"""
        logger.info("Выбираем QR изображение из галереи...")

        try:
            # Выбираем первое доступное изображение
            images = self.driver.find_elements(*self.GALLERY_IMAGES)

            if not images:
                logger.error("QR изображения не найдены в галерее")
                return False

            # Кликаем по первому изображению
            images[0].click()
            time.sleep(3)  # Ждем обработки изображения

            logger.info("QR изображение выбрано")
            return True

        except Exception as e:
            logger.error(f"Ошибка при выборе QR изображения: {e}")
            self.take_screenshot("gallery_selection_error")
            return False

    def wait_for_qr_scan_result(self, timeout=15):
        """Ожидать результата сканирования QR"""
        logger.info("Ожидаем результата сканирования QR...")

        try:
            self.wait.until(
                lambda driver: self.is_element_present(self.PAYMENT_FORM, timeout=2)
            )
            logger.info("QR успешно отсканирован, форма оплаты отображена")
            return True
        except TimeoutException:
            logger.error("QR код не был распознан или форма оплаты не появилась")
            self.take_screenshot("qr_scan_timeout")
            return False

    def get_payment_amount(self):
        """Получить сумму платежа"""
        try:
            amount_element = self.find_element(self.AMOUNT_FIELD)
            amount = amount_element.get_attribute("text") or amount_element.text
            logger.info(f"Сумма платежа: {amount}")
            return amount
        except Exception as e:
            logger.error(f"Не удалось получить сумму платежа: {e}")
            return None

    def get_recipient_info(self):
        """Получить информацию о получателе"""
        try:
            recipient_element = self.find_element(self.RECIPIENT_FIELD)
            recipient = recipient_element.get_attribute("text") or recipient_element.text
            logger.info(f"Получатель: {recipient}")
            return recipient
        except Exception as e:
            logger.error(f"Не удалось получить информацию о получателе: {e}")
            return None

    def click_pay_button(self):
        """Нажать кнопку оплаты"""
        try:
            self.click_element(self.PAY_BUTTON)
            logger.info("Нажата кнопка оплаты")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Не удалось нажать кнопку оплаты: {e}")
            return False

    def cancel_payment(self):
        """Отменить платеж"""
        try:
            self.click_element(self.CANCEL_BUTTON)
            logger.info("Платеж отменен")
            return True
        except Exception as e:
            logger.error(f"Не удалось отменить платеж: {e}")
            return False

    def is_payment_form_displayed(self):
        """Проверить отображение формы оплаты"""
        return self.is_element_present(self.PAYMENT_FORM)