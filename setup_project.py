#!/usr/bin/env python3
"""
Скрипт для настройки проекта автотестов
"""

import os
import sys
from pathlib import Path
from config.settings import *

def check_apk_setup():
    """Проверить настройку APK файла"""
    print("🔍 Проверяем настройку APK файла...")

    if USE_LOCAL_APK:
        if AVAILABLE_APK_PATH:
            print(f"✅ APK файл найден: {AVAILABLE_APK_PATH}")
            print(f"📏 Размер файла: {Path(AVAILABLE_APK_PATH).stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"❌ APK файл не найден!")
            print(f"📝 Инструкции:")
            print(f"   1. Поместите APK файл в директорию: {APK_DIR}")
            print(f"   2. Переименуйте файл в: {APK_FILE_NAME}")
            print(f"   3. Или измените APK_FILE_NAME в config/settings.py")
            print(f"   4. Или установите USE_LOCAL_APK=false в .env файле")
            return False
    else:
        print("🔄 Настроено использование уже установленного приложения")
        print("💡 Убедитесь, что приложение установлено на устройстве/эмуляторе")

    return True

def check_environment():
    """Проверить окружение"""
    print("\n🔍 Проверяем окружение...")

    # Проверяем Python версию
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print(f"❌ Требуется Python 3.8+, у вас: {python_version.major}.{python_version.minor}")
        return False
    else:
        print(f"✅ Python версия: {python_version.major}.{python_version.minor}")

    # Проверяем adb
    adb_result = os.system("adb version > /dev/null 2>&1")
    if adb_result == 0:
        print("✅ ADB доступен")
    else:
        print("❌ ADB не найден или не настроен")
        return False

    return True

def check_directories():
    """Проверить создание директорий"""
    print("\n🔍 Проверяем директории проекта...")

    directories = [
        SCREENSHOTS_DIR,
        REPORTS_DIR,
        TEST_DATA_DIR,
        APK_DIR
    ]

    for directory in directories:
        if directory.exists():
            print(f"✅ {directory.name}/")
        else:
            directory.mkdir(exist_ok=True)
            print(f"🆕 Создана директория: {directory.name}/")

    return True

def show_commands():
    """Показать полезные команды"""
    print("\n📋 Полезные команды для запуска тестов:")
    print("=" * 50)
    print("# Запуск всех тестов:")
    print("pytest -v")
    print()
    print("# Параллельный запуск QR тестов:")
    print("pytest tests/test_qr_payment.py -n 2 -v")
    print()
    print("# Тесты навигации OD:")
    print("pytest tests/test_od_navigation.py -v")
    print()
    print("# Smoke тесты:")
    print("pytest -m smoke -v")
    print()
    print("# С HTML отчетом:")
    print("pytest --html=reports/report.html --self-contained-html")
    print()
    print("# Проверка устройств:")
    print("adb devices")
    print()
    print("# Запуск Appium сервера:")
    print("appium --port 4723")

def main():
    """Основная функция настройки"""
    print("🚀 Настройка проекта автотестов B2B Mobile")
    print("=" * 50)

    success = True

    # Проверки
    success &= check_environment()
    success &= check_directories()
    success &= check_apk_setup()

    if success:
        print("\n✅ Проект настроен успешно!")
        show_commands()
    else:
        print("\n❌ Обнаружены проблемы в настройке проекта")
        sys.exit(1)

if __name__ == "__main__":
    main()