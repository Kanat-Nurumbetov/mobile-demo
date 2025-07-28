from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class OtpPage(BasePage):
    # Локаторы
    OTP_INPUT = (By.ID, "kz.halyk.onlinebank.stage:id/et")
    CONFIRM_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/confirm_otp")
    RESEND_BUTTON = (By.ID, "kz.halyk.onlinebank.stage:id/resend_otp")
    ERROR_MESSAGE = (By.ID, "kz.halyk.onlinebank.stage:id/error_message")

    def enter_otp(self, code):
        """Ввести OTP код"""
        self.enter_text(self.OTP_INPUT, code)
        time.sleep(2)  # Возможна автоотправка

    def click_confirm(self):
        """Нажать подтверждение OTP"""
        if self.is_element_present(self.CONFIRM_BUTTON):
            self.click_element(self.CONFIRM_BUTTON)

    def resend_otp(self):
        """Повторно отправить OTP"""
        self.click_element(self.RESEND_BUTTON)

    def is_otp_error_displayed(self):
        """Проверить ошибку OTP"""
        return self.is_element_present(self.ERROR_MESSAGE)