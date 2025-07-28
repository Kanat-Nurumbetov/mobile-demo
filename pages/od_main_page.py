from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)


class OdMainPage:
    QR_SCANER = (By.XPATH, '//android.view.View[@content-desc="QR"]/android.view.View/android.widget.Image')

    def __init__(self, driver):
        self.driver = driver

    def select_qr_scaner(self):
        """Открыть QR сканер"""
        try:
            logger.info("Открываем QR сканер...")
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.QR_SCANER)
            )
            btn.click()
            logger.info("QR сканер открыт успешно")
            return True
        except TimeoutException:
            logger.error("Не удалось найти кнопку QR сканера")
            return False
        except Exception as e:
            logger.error(f"Ошибка при открытии QR сканера: {e}")
            return False