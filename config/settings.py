import os
from pathlib import Path

# Базовые настройки проекта
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
TEST_DATA_DIR = PROJECT_ROOT / "data"
APK_DIR = PROJECT_ROOT / "apk"

# Режим тестирования
TEST_MODE = os.getenv("TEST_MODE", "local")

# Настройки Appium
APPIUM_SERVER = "http://localhost:4723"
DEVICE_NAME = "emulator-5554"
PLATFORM_NAME = "Android"

# BrowserStack настройки
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Настройки приложения
APP_PACKAGE = "kz.halyk.onlinebank.stage"
APP_ACTIVITY = "kz.halyk.onlinebank.ui_release4.screens.splash.SplashActivity"

# APK файл в проекте
APK_FILE_NAME = "halyk_bank_app.apk"
APK_PATH = APK_DIR / APK_FILE_NAME

# Проверяем наличие APK файла
USE_LOCAL_APK = os.getenv("USE_LOCAL_APK", "true").lower() == "true"

# Тестовые данные для логина
TEST_PHONE = os.getenv("TEST_PHONE", "7771112222")
TEST_OTP = os.getenv("TEST_OTP", "000000")
TEST_PIN = os.getenv("TEST_PIN", "0000")

# Таймауты (в секундах)
DEFAULT_TIMEOUT = 15
LONG_TIMEOUT = 30
SHORT_TIMEOUT = 5

# Настройки скриншотов
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_ON_SUCCESS = False

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "test.log"

# Настройки параллельного запуска
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))


# BrowserStack capabilities
BROWSERSTACK_ANDROID_CAPS = {
    'device': 'Samsung Galaxy S22',
    'os_version': '12.0',
    'project': 'Halyk Bank Tests',
    'build': 'Android Build v1.0',
    'name': 'Halyk Bank Android Test',
    'app': None,  # Будет установлено после загрузки APK
    'browserstack.debug': True,
    'browserstack.video': True,
    'browserstack.networkLogs': True,
    'browserstack.appiumLogs': True
}

BROWSERSTACK_IOS_CAPS = {
    'device': 'iPhone 14',
    'os_version': '16',
    'project': 'Halyk Bank Tests',
    'build': 'iOS Build v1.0',
    'name': 'Halyk Bank iOS Test',
    'app': None,  # Будет установлено после загрузки APK
    'browserstack.debug': True,
    'browserstack.video': True,
    'browserstack.networkLogs': True,
    'browserstack.appiumLogs': True
}

# Создание необходимых директорий
def create_directories():
    """Создать необходимые директории проекта"""
    directories = [
        SCREENSHOTS_DIR,
        REPORTS_DIR,
        TEST_DATA_DIR,
        APK_DIR
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True)

    # Создаем .gitkeep файлы для пустых директорий
    for directory in [SCREENSHOTS_DIR, REPORTS_DIR]:
        gitkeep_file = directory / ".gitkeep"
        if not gitkeep_file.exists():
            gitkeep_file.touch()


# Функция проверки APK
def check_apk_availability():
    """Проверить доступность APK файла"""
    if USE_LOCAL_APK:
        if APK_PATH.exists():
            print(f"✅ APK файл найден: {APK_PATH}")
            return str(APK_PATH)
        else:
            print(f"❌ APK файл не найден: {APK_PATH}")
            print(f"📝 Поместите APK файл в директорию: {APK_DIR}")
            return None
    else:
        print("🔄 Используется уже установленное приложение")
        return None

def validate_browserstack_config():
    """Проверить настройки BrowserStack"""
    if TEST_MODE == "browserstack":
        if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
            print("❌ Не указаны учетные данные BrowserStack!")
            print("📝 Установите BROWSERSTACK_USERNAME и BROWSERSTACK_ACCESS_KEY в .env файле")
            return False
        print("✅ Настройки BrowserStack валидны")
        return True
    return True

# Автоматическое создание директорий при импорте
create_directories()

# Проверка APK при импорте модуля
if USE_LOCAL_APK:
    AVAILABLE_APK_PATH = check_apk_availability()
else:
    AVAILABLE_APK_PATH = None

# Проверка настроек BrowserStack
validate_browserstack_config()
