from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class QrScanerPage:
    gallery = (By.ID, "kz.halyk.onlinebank.stage:id/gallery")

    def __init__(self, driver):
        self.driver = driver

    def qr_gallery_open(self, gallery):
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located(gallery)
        )
