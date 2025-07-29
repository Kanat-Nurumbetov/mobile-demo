import pytest
import logging
import os
import time
from pathlib import Path

# Загружаем переменные окружения
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv не установлен. Переменные окружения будут браться из системы.")

from pages.login_page import LoginPage
from pages.otp_page import OtpPage
from pages.permissions_page import PermissionsPage
from pages.pin_page import PinPage
from utils.qr_generator import make_qr
from data.qr_payloads import QR_PAYLOADS
from config.settings import *

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    # BrowserStack SDK сам создает драйвер и подставляет его как фикстуру
    return request.getfixturevalue("bs_driver") if "bs_driver" in request.fixturenames else None

@pytest.fixture
def qr_image(request, tmp_path, driver):
    """Создание и подготовка QR изображения для теста"""
    distr = request.param
    payload_info = QR_PAYLOADS[distr]
    unique_filename = f"{payload_info['file_name']}"
    local_file = tmp_path / unique_filename
    make_qr(payload_info["text"], local_file)
    return str(local_file)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Обработка результатов тестов и создание скриншотов при ошибках"""
    outcome = yield
    report = outcome.get_result()

    # Обработка результатов для BrowserStack
    if call.when == "call":
        driver = getattr(item, "funcargs", {}).get("driver", None)

        # Создание скриншотов при ошибках
        if report.failed and SCREENSHOT_ON_FAILURE and driver:
            try:
                SCREENSHOTS_DIR.mkdir(exist_ok=True)

                mode_suffix = f"_{driver.test_mode}" if hasattr(driver, 'test_mode') else ""
                screenshot_name = f"{item.name}_failed_{int(time.time())}{mode_suffix}.png"
                screenshot_path = SCREENSHOTS_DIR / screenshot_name

                driver.save_screenshot(str(screenshot_path))
                logger.info(f"📸 Скриншот ошибки сохранен: {screenshot_path}")

            except Exception as e:
                logger.error(f"❌ Не удалось сохранить скриншот: {e}")


@pytest.fixture(autouse=True)
def test_lifecycle(request):
    """Логирование жизненного цикла тестов"""
    test_name = request.node.name
    
    # Пытаемся получить информацию о режиме тестирования
    try:
        driver = request.getfixturevalue('driver') if 'driver' in request.fixturenames else None
        mode_info = f" ({driver.test_mode})" if driver and hasattr(driver, 'test_mode') else ""
    except:
        mode_info = ""

    logger.info(f"▶️ НАЧИНАЕМ ТЕСТ: {test_name}{mode_info}")
    start_time = time.time()

    yield

    duration = time.time() - start_time
    logger.info(f"✅ ТЕСТ ЗАВЕРШЕН: {test_name}{mode_info} (за {duration:.2f}с)")

def pytest_configure(config):
    """Конфигурация pytest"""
    # Регистрируем маркеры
    markers = [
        "smoke: быстрые smoke тесты",
        "qr_payment: тесты QR платежей", 
        "od_navigation: тесты навигации Online Duken",
        "browserstack: тесты для BrowserStack",
        "local: тесты только для локального запуска",
        "regression: регрессионные тесты"
    ]
    
    for marker in markers:
        config.addinivalue_line("markers", marker)

def pytest_collection_modifyitems(config, items):
    """Фильтрация тестов по режиму"""
    test_mode = os.getenv("TEST_MODE", TEST_MODE)
    
    # Добавляем автоматические маркеры в зависимости от режима
    for item in items:
        if test_mode == "browserstack":
            item.add_marker(pytest.mark.browserstack)
        else:
            item.add_marker(pytest.mark.local)