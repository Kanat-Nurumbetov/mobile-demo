import requests
import json
import os
from appium import webdriver
from selenium.common.exceptions import WebDriverException
from config.settings import *

class BrowserStackHelper:
    def __init__(self):
        self.username = BROWSERSTACK_USERNAME
        self.access_key = BROWSERSTACK_ACCESS_KEY
        self.upload_url = "https://api-cloud.browserstack.com/app-automate/upload"
        
    def upload_app(self, app_path):
        """Загрузить APK в BrowserStack"""
        if not os.path.exists(app_path):
            raise FileNotFoundError(f"APK файл не найден: {app_path}")
            
        print(f"📤 Загружаем APK в BrowserStack: {app_path}")
        
        with open(app_path, 'rb') as f:
            files = {'file': f}
            
            response = requests.post(
                self.upload_url,
                files=files,
                auth=(self.username, self.access_key)
            )
            
        if response.status_code == 200:
            result = response.json()
            app_id = result.get('app_url')
            print(f"✅ APK успешно загружен! App ID: {app_id}")
            return app_id
        else:
            print(f"❌ Ошибка загрузки APK: {response.status_code}")
            print(f"Ответ: {response.text}")
            return None
    
    def get_uploaded_apps(self):
        """Получить список загруженных приложений"""
        url = "https://api-cloud.browserstack.com/app-automate/recent_apps"
        
        response = requests.get(url, auth=(self.username, self.access_key))
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Ошибка получения списка приложений: {response.status_code}")
            return None
    
    def create_driver(self, capabilities):
        """Создать драйвер для BrowserStack"""
        try:
            print(f"🚀 Создаем драйвер BrowserStack с capabilities: {capabilities}")
            driver = webdriver.Remote(
                command_executor=BROWSERSTACK_URL,
                desired_capabilities=capabilities
            )
            print("✅ Драйвер BrowserStack создан успешно!")
            return driver
        except WebDriverException as e:
            print(f"❌ Ошибка создания драйвера BrowserStack: {e}")
            return None
    
    def mark_test_status(self, driver, status, reason=""):
        """Отметить статус теста в BrowserStack"""
        script = f'''browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}", "reason": "{reason}"}}}}'''
        try:
            driver.execute_script(script)
            print(f"📝 Статус теста установлен: {status}")
        except Exception as e:
            print(f"⚠️ Не удалось установить статус теста: {e}")


def setup_browserstack_driver():
    """Настроить драйвер для BrowserStack"""
    helper = BrowserStackHelper()
    
    # Загружаем APK если нужно
    app_id = None
    if USE_LOCAL_APK and AVAILABLE_APK_PATH:
        app_id = helper.upload_app(AVAILABLE_APK_PATH)
        if not app_id:
            print("❌ Не удалось загрузить APK, используем уже загруженное приложение")
    
    # Настраиваем capabilities
    caps = BROWSERSTACK_ANDROID_CAPS.copy()
    if app_id:
        caps['app'] = app_id
    else:
        # Используем package/activity для уже установленного приложения
        caps['appPackage'] = APP_PACKAGE
        caps['appActivity'] = APP_ACTIVITY
    
    # Создаем драйвер
    driver = helper.create_driver(caps)
    
    return driver, helper
