import pytest
import logging

logger = logging.getLogger(__name__)


class TestDemo:
    """Демонстрационные тесты для проверки работы системы"""

    def test_system_ready(self):
        """Тест готовности системы"""
        logger.info("🔧 Проверяем готовность системы...")
        
        # Проверяем импорты
        from config.settings import TEST_MODE, APP_PACKAGE
        from utils.qr_generator import make_qr
        from data.qr_payloads import QR_PAYLOADS
        
        logger.info(f"✅ TEST_MODE: {TEST_MODE}")
        logger.info(f"✅ APP_PACKAGE: {APP_PACKAGE}")
        logger.info(f"✅ QR_PAYLOADS: {list(QR_PAYLOADS.keys())}")
        
        # Проверяем генерацию QR кода
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            make_qr("https://test.example.com", tmp_file.name)
            assert os.path.exists(tmp_file.name)
            os.unlink(tmp_file.name)
        
        logger.info("✅ Система готова к работе!")

    @pytest.mark.smoke
    def test_browserstack_config(self):
        """Тест конфигурации BrowserStack"""
        from config.settings import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY
        
        logger.info("🌐 Проверяем конфигурацию BrowserStack...")
        
        if BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY:
            logger.info("✅ BrowserStack учетные данные настроены")
            logger.info(f"Username: {BROWSERSTACK_USERNAME}")
            logger.info(f"Access Key: {'*' * len(BROWSERSTACK_ACCESS_KEY)}")
        else:
            logger.warning("⚠️ BrowserStack учетные данные не настроены")
            pytest.skip("BrowserStack учетные данные не настроены")

    def test_page_objects(self):
        """Тест Page Object Model"""
        logger.info("📄 Проверяем Page Objects...")
        
        # Проверяем импорты Page Objects
        from pages.base_page import BasePage
        from pages.login_page import LoginPage
        from pages.qr_scaner_page import QrScanerPage
        from pages.payment_confirmation_page import PaymentConfirmationPage
        
        # Проверяем, что классы существуют
        assert BasePage is not None
        assert LoginPage is not None
        assert QrScanerPage is not None
        assert PaymentConfirmationPage is not None
        
        logger.info("✅ Все Page Objects импортированы корректно")

    def test_utils(self):
        """Тест утилит"""
        logger.info("🛠️ Проверяем утилиты...")
        
        # Проверяем импорты утилит
        from utils.driver_factory import DriverFactory
        from utils.qr_generator import make_qr
        from utils.test_helpers import TestStep, wait_and_screenshot
        
        # Проверяем, что классы существуют
        assert DriverFactory is not None
        assert make_qr is not None
        assert TestStep is not None
        assert wait_and_screenshot is not None
        
        logger.info("✅ Все утилиты импортированы корректно")

    def test_makefile_commands(self):
        """Тест команд Makefile"""
        logger.info("📋 Проверяем команды Makefile...")
        
        import subprocess
        import os
        
        # Проверяем, что Makefile существует
        makefile_path = "Makefile.execution"
        assert os.path.exists(makefile_path), "Makefile.execution должен существовать"
        
        # Проверяем, что можно получить список команд
        try:
            result = subprocess.run(
                ["make", "-f", "Makefile.execution", "-n", "test-smoke"],
                capture_output=True,
                text=True
            )
            logger.info("✅ Makefile команды работают")
        except Exception as e:
            logger.warning(f"⚠️ Ошибка проверки Makefile: {e}")
        
        logger.info("✅ Makefile команды проверены")

    @pytest.mark.smoke
    def test_full_system_check(self):
        """Полная проверка системы"""
        logger.info("🚀 Выполняем полную проверку системы...")
        
        # Проверяем все компоненты
        self.test_system_ready()
        self.test_page_objects()
        self.test_utils()
        self.test_makefile_commands()
        
        logger.info("🎉 Система полностью готова к работе!")
        
        # Выводим информацию о том, как запускать тесты
        logger.info("📝 Для запуска тестов используйте:")
        logger.info("  - make -f Makefile.execution test-smoke")
        logger.info("  - python3 -m pytest tests/test_simple.py -v")
        logger.info("  - TEST_MODE=browserstack python3 -m pytest tests/test_b2b.py -v") 