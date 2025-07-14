from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class OdMainPage:
    QR_SCANER = (By.XPATH, '//android.view.View[@content-desc="QR"]/android.view.View/android.widget.Image')
    def __init__(self, driver):
        self.driver = driver

    def select_qr_scaner(self):
        btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.QR_SCANER))
        btn.click()

