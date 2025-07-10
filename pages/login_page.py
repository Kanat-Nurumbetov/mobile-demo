from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    PHONE_INPUT = (By.ID, "kz.halyk.onlinebank.stage:id/phone_input")
    LOGIN_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/login_button")

    def __init__(self, driver):
        self.driver = driver

    def enter_phone(self, phone):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.PHONE_INPUT)
        )
        field.send_keys(phone)

    def click_login(self):
        btn = self.driver.find_element(*self.LOGIN_BUTTON)
        btn.click()
