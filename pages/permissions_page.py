from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PermissionsPage:
    NEXT_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/successButtonNext")

    def __init__(self, driver):
        self.driver = driver

    def click_next(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NEXT_BUTTON)
        )
        btn.click()
