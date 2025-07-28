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

from utils.driver_factory import DriverFactory
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

@pytest.fixture(scope="session")
def test_mode():
    """Получить режим тестирования из переменной окружения"""
    return os.getenv("TEST_MODE", TEST_MODE)

@pytest.fixture(scope="function")
def driver(test_mode):
    """Создание драйвера (локального или BrowserStack)"""
    logger.info(f"🚀 Создаем драйвер в режиме: {test_mode}")
    
    driver_instance, helper = DriverFactory.create_driver(test_mode)
    
    if not driver_instance:
        pytest.fail(f"❌ Не удалось создать драйвер в режиме: {test_mode}")
    
    # Добавляем атрибуты к драйверу
    driver_instance.browserstack_helper = helper
    driver_instance.test_mode = test_mode
    driver_instance.implicitly_wait(DEFAULT_TIMEOUT)
    
    yield driver_instance
    
    # Cleanup
    try:
        logger.info("🧹 Закрываем драйвер...")
        driver_instance.quit()
    except Exception as e:
        logger.warning(f"⚠️ Ошибка при закрытии драйвера: {e}")

@pytest.fixture(scope="function")
def login(driver):
    """Фикстура авторизации"""
    mode_suffix = f"_{driver.test_mode}"
    logger.info(f"🔐 Выполняем авторизацию ({driver.test_mode})...")
    
    try:
        SCREENSHOTS_DIR.mkdir(exist_ok=True)
        
        # Стартовый скриншот
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"login_start{mode_suffix}.png"))

        # Авторизация
        login_page = LoginPage(driver)
        login_page.enter_phone(TEST_PHONE)
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"phone_entered{mode_suffix}.png"))

        login_page.click_login()
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"login_clicked{mode_suffix}.png"))

        # OTP
        otp_page = OtpPage(driver)
        otp_page.enter_otp(TEST_OTP)
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"otp_entered{mode_suffix}.png"))

        # PIN
        pin_page = PinPage(driver)
        pin_page.wait_for_pin_screen()
        pin_page.enter_pin(TEST_PIN)
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"first_pin{mode_suffix}.png"))

        # Подтверждение PIN
        pin_page.enter_pin(TEST_PIN)
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"second_pin{mode_suffix}.png"))

        # Разрешения
        permissions_page = PermissionsPage(driver)
        permissions_page.click_next()
        driver.save_screenshot(str(SCREENSHOTS_DIR / f"permissions{mode_suffix}.png"))

        # Отмечаем успех в BrowserStack
        if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
            driver.browserstack_helper.mark_test_status(
                driver, "passed", "Авторизация выполнена успешно"
            )

        logger.info(f"✅ Авторизация успешна ({driver.test_mode})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка авторизации: {e}")
        
        # Скриншот ошибки
        error_screenshot = SCREENSHOTS_DIR / f"login_error{mode_suffix}_{int(time.time())}.png"
        driver.save_screenshot(str(error_screenshot))
        
        # Отмечаем ошибку в BrowserStack
        if hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
            driver.browserstack_helper.mark_test_status(
                driver, "failed", f"Ошибка авторизации: {str(e)}"
            )
        
        pytest.fail(f"Не удалось авторизоваться: {e}")

@pytest.fixture
def qr_image(request, tmp_path, driver):
    """Создание и подготовка QR изображения для теста"""
    distr = request.param
    payload_info = QR_PAYLOADS[distr]
    
    mode_suffix = f"_{driver.test_mode}"
    logger.info(f"📱 Создаем QR для дистрибьютора: {distr} ({driver.test_mode})")

    # Генерируем уникальное имя файла
    worker_id = getattr(request.config, 'workerinput', {}).get('workerid', 'master')
    unique_filename = f"{worker_id}_{payload_info['file_name']}{mode_suffix}.png"

    # Создаем QR локально
    local_file = tmp_path / unique_filename
    make_qr(payload_info["text"], local_file)

    if driver.test_mode == "browserstack":
        # Для BrowserStack возвращаем локальный путь
        # В реальном проекте здесь может быть логика загрузки в облачное хранилище
        logger.info(f"📱 QR файл создан для BrowserStack: {local_file}")
        return str(local_file)
    else:
        # Для локального тестирования загружаем на устройство
        device_file = f"/sdcard/Download/{unique_filename}"
        
        os.system("adb shell mkdir -p /sdcard/Download/")
        result = os.system(f"adb push '{local_file}' '{device_file}'")
        
        if result != 0:
            logger.error(f"❌ Ошибка загрузки QR файла на устройство")
            raise Exception("Не удалось загрузить QR файл")

        logger.info(f"✅ QR файл загружен на устройство: {device_file}")
        return device_file


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Обработка результатов тестов и создание скриншотов при ошибках"""
    outcome = yield
    report = outcome.get_result()

    # Обработка результатов для BrowserStack
    if call.when == "call":
        driver = getattr(item, "funcargs", {}).get("driver", None)

        if driver and hasattr(driver, 'browserstack_helper') and driver.browserstack_helper:
            if call.excinfo is None:  # Тест прошел
                driver.browserstack_helper.mark_test_status(
                    driver, "passed", f"Тест {item.name} выполнен успешно"
                )
            else:  # Тест упал
                error_msg = str(call.excinfo.value) if call.excinfo.value else "Неизвестная ошибка"
                driver.browserstack_helper.mark_test_status(
                    driver, "failed", f"Тест {item.name}: {error_msg}"
                )

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