import pytest
import logging
from pages.main_page_ob import MainPage
from pages.od_main_page import OdMainPage
from pages.qr_scaner_page import QrScanerPage
from pages.payment_confirmation_page import PaymentConfirmationPage
from utils.test_helpers import TestStep, wait_and_screenshot
from config.settings import TEST_MODE

logger = logging.getLogger(__name__)


class TestQrPaymentBrowserStack:
    """Тесты QR сканирования для BrowserStack и локального запуска"""

    @TestStep("Навигация к QR сканеру")
    def navigate_to_qr_scanner(self, driver, login):
        """Перейти к QR сканеру через OD"""
        main = MainPage(driver)
        main.wait_for_main_page()
        main.dismiss_hint()
        main.dismiss_hint()

        wait_and_screenshot(driver, f"main_page_loaded_{driver.test_mode}")

        main.go_to_online_duken()
        wait_and_screenshot(driver, f"od_main_opened_{driver.test_mode}")

        od = OdMainPage(driver)

        assert od.select_qr_scaner(), "Не удалось открыть QR сканер"
        wait_and_screenshot(driver, f"qr_scanner_opened_{driver.test_mode}")

        return od

    @pytest.mark.parametrize(
        "qr_image",
        ["distrA", "distrB"],
        indirect=True,
        ids=["Universal-QR", "Megapolis-QR"]
    )
    def test_full_qr_payment_flow_universal(self, driver, qr_image, login):
        """Универсальный тест QR платежа (работает локально и в BrowserStack)"""

        test_name = f"QR Payment Flow - {driver.test_mode}"
        logger.info(f"🚀 Запуск теста: {test_name}")

        try:
            # Навигация к QR сканеру
            self.navigate_to_qr_scanner(driver, login)

            # Инициализация страниц
            scanner = QrScanerPage(driver)
            confirmation = PaymentConfirmationPage(driver)

            # Ожидание загрузки QR сканера
            scanner.wait_for_qr_scanner()
            scanner.allow_camera_permission()

            # Открытие галереи и выбор QR
            scanner.open_gallery()
            wait_and_screenshot(driver, f"gallery_opened_{driver.test_mode}")

            assert scanner.select_qr_from_gallery(qr_image), \
                "Не удалось выбрать QR изображение из галереи"
            wait_and_screenshot(driver, f"qr_image_selected_{driver.test_mode}")

            # Ожидание результата сканирования
            assert scanner.wait_for_qr_scan_result(), \
                "QR код не был успешно отсканирован"
            wait_and_screenshot(driver, f"qr_scan_result_{driver.test_mode}")

            # Проверка формы оплаты
            assert scanner.is_payment_form_displayed(), \
                "Форма оплаты не отображается после сканирования"

            # Получение информации о платеже
            amount = scanner.get_payment_amount()
            recipient = scanner.get_recipient_info()

            logger.info(f"Данные платежа - Сумма: {amount}, Получатель: {recipient}")

            # Клик по кнопке оплаты
            assert scanner.click_pay_button(), \
                "Не удалось нажать кнопку оплаты"
            wait_and_screenshot(driver, f"payment_button_clicked_{driver.test_mode}")

            # Подтверждение платежа
            confirmation.wait_for_confirmation_page()
            payment_info = confirmation.get_payment_info()

            logger.info(f"Информация для подтверждения: {payment_info}")

            # Подтверждение операции
            assert confirmation.confirm_payment(), \
                "Не удалось подтвердить платеж"
            wait_and_screenshot(driver, f"payment_confirmed_{driver.test_mode}")

            # Ожидание результата
            result = confirmation.wait_for_payment_result(timeout=30)

            if result == "success":
                transaction_id = confirmation.get_transaction_id()
                logger.info(f"✅ Платеж успешен! ID транзакции: {transaction_id}")
                wait_and_screenshot(driver, f"payment_success_{driver.test_mode}")

                # Отмечаем успех в BrowserStack
                if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                    driver.browserstack_helper.mark_test_status(
                        driver, "passed", f"QR платеж успешно выполнен. ID: {transaction_id}"
                    )

            elif result == "error":
                error_msg = confirmation.get_error_message()
                logger.error(f"❌ Платеж не выполнен: {error_msg}")
                wait_and_screenshot(driver, f"payment_error_{driver.test_mode}")

                # Отмечаем ошибку в BrowserStack
                if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                    driver.browserstack_helper.mark_test_status(
                        driver, "failed", f"Ошибка платежа: {error_msg}"
                    )

                pytest.fail(f"Платеж не выполнен: {error_msg}")

            else:  # timeout
                wait_and_screenshot(driver, f"payment_timeout_{driver.test_mode}")

                # Отмечаем таймаут в BrowserStack
                if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                    driver.browserstack_helper.mark_test_status(
                        driver, "failed", "Превышено время ожидания результата платежа"
                    )

                pytest.fail("Превышено время ожидания результата платежа")

        except Exception as e:
            logger.error(f"❌ Ошибка в тесте: {e}")

            # Делаем скриншот ошибки
            wait_and_screenshot(driver, f"test_error_{driver.test_mode}")

            # Отмечаем ошибку в BrowserStack
            if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                driver.browserstack_helper.mark_test_status(
                    driver, "failed", f"Ошибка теста: {str(e)}"
                )

            raise

    @pytest.mark.smoke
    def test_qr_scanner_ui_elements_universal(self, driver, login):
        """Универсальный smoke test UI элементов QR сканера"""

        test_name = f"QR Scanner UI - {driver.test_mode}"
        logger.info(f"🔍 Запуск smoke теста: {test_name}")

        try:
            self.navigate_to_qr_scanner(driver, login)

            scanner = QrScanerPage(driver)
            scanner.wait_for_qr_scanner()

            # Проверяем наличие основных элементов
            assert scanner.is_element_present(scanner.QR_FRAME), \
                "QR рамка не отображается"

            assert scanner.is_element_present(scanner.GALLERY_BUTTON), \
                "Кнопка галереи не отображается"

            wait_and_screenshot(driver, f"qr_scanner_ui_{driver.test_mode}")

            # Отмечаем успех в BrowserStack
            if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                driver.browserstack_helper.mark_test_status(
                    driver, "passed", "UI элементы QR сканера отображаются корректно"
                )

            logger.info("✅ Smoke test UI прошел успешно")

        except Exception as e:
            logger.error(f"❌ Ошибка в smoke тесте: {e}")

            # Отмечаем ошибку в BrowserStack
            if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
                driver.browserstack_helper.mark_test_status(
                    driver, "failed", f"Ошибка UI теста: {str(e)}"
                )

            raise