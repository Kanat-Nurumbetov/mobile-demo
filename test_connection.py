#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к Appium и приложению
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

def test_connection():
    print("🔍 Проверяем подключение к Appium...")

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"  # Замените на ваше устройство
    options.app_package = "kz.halyk.onlinebank.stage"
    options.app_activity = "kz.halyk.onlinebank.ui_release4.screens.splash.SplashActivity"
    options.automation_name = "UiAutomator2"
    options.auto_grant_permissions = True
    options.no_reset = True

    # Если используете локальный APK
    # options.app = "/path/to/your/app.apk"

    try:
        print("📱 Подключаемся к устройству...")
        driver = webdriver.Remote('http://localhost:4723', options=options)

        print("✅ Подключение успешно!")
        print(f"📋 Информация о сессии: {driver.session_id}")

        # Делаем скриншот для проверки
        driver.save_screenshot("connection_test.png")
        print("📸 Скриншот сохранен: connection_test.png")

        # Получаем информацию о приложении
        current_package = driver.current_package
        current_activity = driver.current_activity

        print(f"📦 Текущий пакет: {current_package}")
        print(f"🔧 Текущая активность: {current_activity}")

        time.sleep(2)

        driver.quit()
        print("✅ Тест подключения прошел успешно!")
        return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\n💡 Проверьте:")
        print("   - Запущен ли Appium сервер (appium --port 4723)")
        print("   - Подключено ли устройство (adb devices)")
        print("   - Правильно ли указан пакет приложения")
        print("   - Установлено ли приложение на устройстве")
        return False

if __name__ == "__main__":
    test_connection()