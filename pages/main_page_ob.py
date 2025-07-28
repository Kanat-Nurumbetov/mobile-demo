from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time
import logging
import os

logger = logging.getLogger(__name__)

class MainPage(BasePage):
    # Локаторы главной страницы
    CONTRACT_NAME = (By.ID, "kz.halyk.onlinebank.stage:id/contract_name_text_view")
    ONLINE_DUKEN_BTN = (By.XPATH, '(//android.view.ViewGroup[@resource-id="kz.halyk.onlinebank.stage:id/container"])[1]')

    # Альтернативные локаторы для кнопки OD
    ONLINE_DUKEN_ALT = (By.XPATH, '//*[contains(@text, "Online") or contains(@content-desc, "Online")]')

    # Элементы подсказок и хинтов
    HINT_OVERLAY = (By.ID, "kz.halyk.onlinebank.stage:id/hint_overlay")
    CLOSE_HINT_BTN = (By.ID, "kz.halyk.onlinebank.stage:id/close_hint")

    # Элементы OD marketplace
    MARKETPLACE_LOGO = (By.XPATH, '//*[@text="main logo"]')
    MARKETPLACE_ALT = (By.ID, "kz.halyk.onlinebank.stage:id/marketplace_container")

    def wait_for_main_page(self, timeout=15):
        """Ожидать загрузки главной страницы"""
        logger.info("Ожидаем загрузки главной страницы...")
        self.find_element(self.CONTRACT_NAME)
        logger.info("Главная страница загружена")

    def dismiss_hint(self, timeout=3):
        """Закрыть подсказки/хинты более надежным способом"""
        try:
            # Сначала пробуем найти кнопку закрытия хинта
            if self.is_element_present(self.CLOSE_HINT_BTN, timeout=timeout):
                self.click_element(self.CLOSE_HINT_BTN)
                logger.info("Закрыли хинт через кнопку")
                time.sleep(1)
                return True

            # Если кнопки нет, пробуем тап по области
            elif self.is_element_present(self.HINT_OVERLAY, timeout=timeout):
                size = self.driver.get_window_size()
                x = size['width'] // 2
                y = int(size['height'] * 0.1)
                os.system(f"adb shell input tap {x} {y}")
                logger.info("Закрыли хинт через тап")
                time.sleep(1)
                return True

        except Exception as e:
            logger.info(f"Хинт не найден или уже закрыт: {e}")

        return False

    def is_text_present(self, expected_text, timeout=10):
        """Проверить наличие текста на странице"""
        self.wait_for_main_page(timeout=timeout)
        time.sleep(1)

        all_text_views = self.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
        for el in all_text_views:
            try:
                element_text = el.text.strip()
                if expected_text in element_text:
                    logger.info(f"Текст '{expected_text}' найден в '{element_text}'")
                    return True
            except Exception:
                continue

        logger.warning(f"Текст '{expected_text}' не найден на странице")
        return False

    def select_company_by_name(self, name):
        """Выбрать компанию по имени"""
        try:
            self.click_element(self.CONTRACT_NAME)

            # Ждем появления списка компаний
            time.sleep(2)

            if self.is_text_present(name):
                elems = self.driver.find_elements(By.CLASS_NAME, "android.widget.TextView")
                for el in elems:
                    try:
                        if name in el.text.strip():
                            el.click()
                            logger.info(f"Выбрана компания: {name}")
                            return True
                    except Exception:
                        continue

            logger.warning(f"Компания '{name}' не найдена")
            return False

        except Exception as e:
            logger.error(f"Ошибка при выборе компании: {e}")
            return False

    def go_to_online_duken(self):
        """Перейти в Online Duken"""
        logger.info("Переходим в Online Duken...")

        # Пробуем разные локаторы для кнопки OD
        locators = [self.ONLINE_DUKEN_BTN, self.ONLINE_DUKEN_ALT]

        for i, locator in enumerate(locators):
            try:
                logger.info(f"Попытка {i+1}: ищем кнопку OD по локатору {locator}")
                btn = self.find_clickable_element(locator)
                btn.click()
                logger.info("Кнопка Online Duken нажата")
                time.sleep(3)  # Ждем загрузки OD
                return True

            except Exception as e:
                logger.warning(f"Локатор {i+1} не сработал: {e}")
                continue

        logger.error("Не удалось найти кнопку Online Duken")
        raise Exception("Кнопка Online Duken не найдена")

    def is_marketplace_loaded(self, timeout=15):
        """Проверить загрузку marketplace"""
        logger.info("Проверяем загрузку Online Duken marketplace...")

        # Пробуем разные способы определить загрузку OD
        try:
            # Основной способ - поиск логотипа
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.MARKETPLACE_LOGO)
            )
            logger.info("Marketplace загружен (найден логотип)")
            return True

        except TimeoutException:
            try:
                # Альтернативный способ
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.MARKETPLACE_ALT)
                )
                logger.info("Marketplace загружен (найден контейнер)")
                return True

            except TimeoutException:
                logger.error("Marketplace не загрузился")
                return False

    def is_od_button_visible(self):
        """Проверить видимость кнопки OD"""
        return self.is_element_present(self.ONLINE_DUKEN_BTN) or \
            self.is_element_present(self.ONLINE_DUKEN_ALT)

    def is_od_button_enabled(self):
        """Проверить доступность кнопки OD для клика"""
        try:
            btn = self.find_element(self.ONLINE_DUKEN_BTN)
            return btn.is_enabled()
        except:
            try:
                btn = self.find_element(self.ONLINE_DUKEN_ALT)
                return btn.is_enabled()
            except:
                return False