from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OtpPage:
    OTP_INPUT = (By.ID, "kz.halyk.onlinebank.stage:id/et")
    # Можно добавить локаторы для кнопки "Подтвердить" или автоматической отправки

    def __init__(self, driver):
        self.driver = driver

    def enter_otp(self, code):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.OTP_INPUT)
        )
        field.send_keys(code)
