from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.settings import *
from browserstack_helper import BrowserStackHelper
import logging

logger = logging.getLogger(__name__)

class DriverFactory:
    """Фабрика для создания драйверов"""
    
    @staticmethod
    def create_driver(test_mode=None):
        """Создать драйвер в зависимости от режима тестирования"""
        mode = test_mode or TEST_MODE
        
        if mode == "browserstack":
            return DriverFactory._create_browserstack_driver()
        else:
            return DriverFactory._create_local_driver()
    
    @staticmethod
    def _create_local_driver():
        """Создать локальный драйвер"""
        logger.info("🔧 Создаем локальный драйвер...")
        
        options = UiAutomator2Options()
        options.platform_name = PLATFORM_NAME
        options.device_name = DEVICE_NAME
        options.app_package = APP_PACKAGE
        options.app_activity = APP_ACTIVITY
        options.automation_name = "UiAutomator2"
        options.auto_grant_permissions = True
        options.no_reset = True
        
        # Если используется локальный APK
        if USE_LOCAL_APK and AVAILABLE_APK_PATH:
            options.app = AVAILABLE_APK_PATH
        
        driver = webdriver.Remote(APPIUM_SERVER, options=options)
        logger.info("✅ Локальный драйвер создан успешно")
        
        return driver, None
    
    @staticmethod
    def _create_browserstack_driver():
        """Создать BrowserStack драйвер"""
        logger.info("🌐 Создаем BrowserStack драйвер...")
        
        helper = BrowserStackHelper()
        
        # Загружаем APK если нужно
        app_id = None
        if USE_LOCAL_APK and AVAILABLE_APK_PATH:
            app_id = helper.upload_app(AVAILABLE_APK_PATH)
            if not app_id:
                logger.warning("⚠️ Не удалось загрузить APK, используем установленное приложение")
        
        # Настраиваем capabilities
        caps = BROWSERSTACK_ANDROID_CAPS.copy()
        if app_id:
            caps['app'] = app_id
        else:
            caps['appPackage'] = APP_PACKAGE
            caps['appActivity'] = APP_ACTIVITY
        
        # Создаем драйвер
        driver = helper.create_driver(caps)
        
        if driver:
            logger.info("✅ BrowserStack драйвер создан успешно")
        else:
            logger.error("❌ Не удалось создать BrowserStack драйвер")
            
        return driver, helper
