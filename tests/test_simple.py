import pytest
import logging

logger = logging.getLogger(__name__)


class TestSimple:
    """Простые тесты для проверки базовой функциональности"""

    def test_config_loading(self):
        """Тест загрузки конфигурации"""
        from config.settings import TEST_MODE, APP_PACKAGE, BROWSERSTACK_USERNAME
        
        logger.info(f"TEST_MODE: {TEST_MODE}")
        logger.info(f"APP_PACKAGE: {APP_PACKAGE}")
        logger.info(f"BROWSERSTACK_USERNAME: {BROWSERSTACK_USERNAME}")
        
        assert TEST_MODE in ["local", "browserstack"], "TEST_MODE должен быть local или browserstack"
        assert APP_PACKAGE == "kz.halyk.onlinebank.stage", "APP_PACKAGE должен быть корректным"
        
        logger.info("✅ Конфигурация загружена корректно")

    def test_qr_generator(self):
        """Тест генератора QR кодов"""
        from utils.qr_generator import make_qr
        import tempfile
        import os
        
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            qr_text = "https://test.example.com"
            make_qr(qr_text, tmp_file.name)
            
            # Проверяем, что файл создан
            assert os.path.exists(tmp_file.name), "QR файл должен быть создан"
            assert os.path.getsize(tmp_file.name) > 0, "QR файл не должен быть пустым"
            
            # Удаляем временный файл
            os.unlink(tmp_file.name)
            
        logger.info("✅ QR генератор работает корректно")

    def test_qr_payloads(self):
        """Тест загрузки QR payloads"""
        from data.qr_payloads import QR_PAYLOADS
        
        assert "distrA" in QR_PAYLOADS, "Должен быть дистрибьютор A"
        assert "distrB" in QR_PAYLOADS, "Должен быть дистрибьютор B"
        
        for distr, payload in QR_PAYLOADS.items():
            assert "text" in payload, f"Payload для {distr} должен содержать text"
            assert "file_name" in payload, f"Payload для {distr} должен содержать file_name"
            assert payload["text"].startswith("http"), f"QR текст для {distr} должен быть URL"
        
        logger.info("✅ QR payloads загружены корректно")

    def test_browserstack_helper(self):
        """Тест BrowserStack helper"""
        from browserstack_helper import BrowserStackHelper
        
        helper = BrowserStackHelper()
        
        # Проверяем, что helper создан
        assert helper.username is not None, "Username должен быть установлен"
        assert helper.access_key is not None, "Access key должен быть установлен"
        
        logger.info("✅ BrowserStack helper создан корректно")

    @pytest.mark.smoke
    def test_basic_functionality(self):
        """Smoke тест базовой функциональности"""
        # Проверяем импорты
        from pages.base_page import BasePage
        from pages.login_page import LoginPage
        from pages.qr_scaner_page import QrScanerPage
        
        # Проверяем, что классы существуют
        assert BasePage is not None, "BasePage должен быть импортирован"
        assert LoginPage is not None, "LoginPage должен быть импортирован"
        assert QrScanerPage is not None, "QrScanerPage должен быть импортирован"
        
        logger.info("✅ Все основные модули импортированы корректно") 