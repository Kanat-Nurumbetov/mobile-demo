import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def wait_and_screenshot(driver, name, delay=2):
    """Сделать паузу и скриншот"""
    time.sleep(delay)
    screenshot_path = f"screenshots/{name}_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)
    logger.info(f"Скриншот: {screenshot_path}")
    return screenshot_path

def retry_action(func, max_attempts=3, delay=2):
    """Повторить действие несколько раз при неудаче"""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1} неудачна: {e}")
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)

def clean_screenshots_folder():
    """Очистить папку скриншотов"""
    screenshots_dir = Path("screenshots")
    if screenshots_dir.exists():
        for file in screenshots_dir.glob("*.png"):
            try:
                file.unlink()
                logger.info(f"Удален скриншот: {file}")
            except Exception as e:
                logger.warning(f"Не удалось удалить {file}: {e}")

class TestStep:
    """Декоратор для логирования шагов теста"""
    def __init__(self, description):
        self.description = description
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            logger.info(f"ШАГ: {self.description}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"ШАГ ВЫПОЛНЕН: {self.description}")
                return result
            except Exception as e:
                logger.error(f"ОШИБКА В ШАГЕ: {self.description} - {e}")
                raise
        return wrapper
