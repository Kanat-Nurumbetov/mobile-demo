from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PinPage:
    # Кнопки можно искать по тексту!
    def __init__(self, driver):
        self.driver = driver

    def enter_pin(self, pin: str):
        for digit in pin:
            # Кнопки имеют текст, ищем по нему
            btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//android.widget.TextView[@text='0']"))
            )
            btn.click()
