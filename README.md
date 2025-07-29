# 🏦 B2B Mobile Testing Suite

Автоматизированное тестирование мобильного банковского приложения с фокусом на QR-платежи и B2B функциональность.

## 🚀 Особенности

- ✅ **Page Object Model** - структурированная архитектура тестов
- 📱 **Appium интеграция** - тестирование мобильного приложения
- 🔍 **QR Code Testing** - полное покрытие QR сканирования и платежей
- 📊 **HTML Reports** - детальные отчеты с скриншотами
- 🎯 **Параметризированные тесты** - тестирование разных дистрибьюторов
- 📸 **Автоскриншоты** - снимки экрана при ошибках и ключевых моментах
- 🌐 **BrowserStack интеграция** - тестирование на реальных устройствах
- 📱 **Мульти-устройственное тестирование** - поддержка разных Android устройств
- 🔄 **Параллельное выполнение** - ускорение тестирования

## 📁 Структура проекта

```
mobile-demo/
├── apk/                          # APK файлы приложения
├── config/                        # Конфигурация проекта
│   └── settings.py               # Основные настройки
├── data/                         # Тестовые данные
│   └── qr_payloads.py           # QR коды для тестирования
├── pages/                        # Page Object Model
│   ├── base_page.py             # Базовый класс страницы
│   ├── login_page.py            # Страница авторизации
│   ├── main_page_ob.py          # Главная страница
│   ├── od_main_page.py          # Страница Online Duken
│   ├── qr_scaner_page.py        # QR сканер
│   └── payment_confirmation_page.py # Подтверждение платежа
├── tests/                        # Тестовые файлы
│   └── test_b2b.py             # Основные тесты B2B
├── utils/                        # Утилиты
│   ├── driver_factory.py        # Фабрика драйверов
│   ├── qr_generator.py          # Генератор QR кодов
│   └── test_helpers.py          # Вспомогательные функции
├── reports/                      # Отчеты тестирования
├── screenshots/                  # Скриншоты
├── browserstack_helper.py        # Интеграция с BrowserStack
├── conftest.py                   # Конфигурация pytest
├── requirements.txt              # Зависимости Python
└── Makefile.execution           # Команды для запуска
```

## 🛠️ Установка и настройка

### 1. Клонирование и установка зависимостей

```bash
git clone <repository-url>
cd mobile-demo
make install
```

### 2. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и настройте параметры:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
# BrowserStack учетные данные
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key

# Режим тестирования
TEST_MODE=browserstack  # или local

# Тестовые данные
TEST_PHONE=7771112222
TEST_OTP=000000
TEST_PIN=0000
```

### 3. Подготовка APK файла

Поместите APK файл в директорию `apk/`:

```bash
cp path/to/your/app.apk apk/halyk_bank_app.apk
```

## 🚀 Запуск тестов

### Локальное тестирование

```bash
# Обычный запуск
make test-b2b-local

# Параллельный запуск
make test-parallel

# Smoke тесты
make test-smoke
```

### BrowserStack тестирование

```bash
# Проверка конфигурации BrowserStack
make browserstack-check

# Загрузка APK в BrowserStack
make browserstack-upload

# Запуск тестов в BrowserStack
make test-qr-browserstack

# Smoke тесты в BrowserStack
make test-smoke-browserstack
```

### Мульти-устройственное тестирование

```bash
# Тестирование на разных устройствах
make test-multidevice

# UI тесты на разных устройствах
make test-ui-multidevice

# Тестирование на конкретном устройстве
make test-samsung-s22
make test-pixel-6

# Параллельное тестирование на устройствах
make test-parallel-devices
```

### Отладка и профилирование

```bash
# Отладка локально
make debug-local

# Отладка в BrowserStack
make debug-browserstack

# Профилирование тестов
make profile-test

# Проверка конфигурации
make check-config
```

## 📱 Поддерживаемые устройства

### Android устройства в BrowserStack

- **Samsung Galaxy S22** (Android 12.0)
- **Samsung Galaxy S21** (Android 11.0)
- **Google Pixel 6** (Android 12.0)
- **OnePlus 9** (Android 11.0)

### Локальные устройства

- Эмулятор Android
- Физические устройства через ADB

## 🔧 Конфигурация

### Основные настройки (`config/settings.py`)

```python
# Режим тестирования
TEST_MODE = "browserstack"  # или "local"

# BrowserStack настройки
BROWSERSTACK_USERNAME = "your_username"
BROWSERSTACK_ACCESS_KEY = "your_access_key"

# Настройки приложения
APP_PACKAGE = "kz.halyk.onlinebank.stage"
APP_ACTIVITY = "kz.halyk.onlinebank.ui_release4.screens.splash.SplashActivity"

# Таймауты
DEFAULT_TIMEOUT = 15
LONG_TIMEOUT = 30
SHORT_TIMEOUT = 5
```

### QR коды для тестирования (`data/qr_payloads.py`)

```python
QR_PAYLOADS = {
    "distrA": {
        "text": "https://public.test.onlinebank.kz/applink/b2b/distributor/...",
        "file_name": "Universal.png"
    },
    "distrB": {
        "text": "https://homebank.kz/payments/megapolisKZ?...",
        "file_name": "Megapolis.png"
    }
}
```

## 📊 Отчеты

### HTML отчеты

```bash
# Генерация HTML отчета
make test-qr-report

# Отчеты сохраняются в директории reports/
```

### Allure отчеты

```bash
# Генерация Allure отчета
make test-allure

# Просмотр отчета
make allure-report
```

### BrowserStack отчеты

Все тесты автоматически отправляют результаты в BrowserStack с:
- Видеозаписями сессий
- Логами устройства
- Скриншотами ошибок
- Детальной информацией о тестах

## 🔍 Мониторинг и отладка

### Проверка доступности устройств

```bash
# Проверка статуса устройств BrowserStack
make browserstack-devices

# Мониторинг в реальном времени
make monitor-browserstack
```

### Проверка загруженных приложений

```bash
# Список загруженных APK
make browserstack-apps
```

### Проверка подключения

```bash
# Тест подключения к BrowserStack
make test-connection
```

## 🧪 Типы тестов

### 1. Smoke тесты
- Проверка основных UI элементов
- Быстрая валидация функциональности
- Тестирование на разных устройствах

### 2. QR платежи
- Полный цикл QR сканирования
- Тестирование разных дистрибьюторов
- Проверка форм оплаты

### 3. Навигация
- Тестирование навигации по приложению
- Проверка переходов между экранами

### 4. Авторизация
- Тестирование процесса входа
- Проверка OTP и PIN кодов

## 🚨 Обработка ошибок

### Автоматические скриншоты
- При ошибках тестов
- При таймаутах
- При критических моментах

### Логирование
- Детальные логи всех операций
- Информация о сессиях BrowserStack
- Отслеживание времени выполнения

### BrowserStack интеграция
- Автоматическая отметка статуса тестов
- Детальная информация об ошибках
- Видеозаписи проблемных сессий

## 🔄 CI/CD интеграция

### GitHub Actions

```yaml
name: Mobile Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: make install
      - name: Run BrowserStack tests
        run: make ci-test-browserstack
        env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
```

### Jenkins

```groovy
pipeline {
    agent any
    environment {
        BROWSERSTACK_USERNAME = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
    }
    stages {
        stage('Install') {
            steps {
                sh 'make install'
            }
        }
        stage('Test') {
            steps {
                sh 'make ci-test-browserstack'
            }
        }
    }
}
```

## 📈 Метрики и аналитика

### Время выполнения тестов
- Отслеживание времени каждого теста
- Сравнение производительности на разных устройствах
- Анализ трендов

### Стабильность тестов
- Процент успешных запусков
- Анализ флаки тестов
- Мониторинг стабильности

### Покрытие функциональности
- Отслеживание покрытия QR функциональности
- Мониторинг покрытия разных дистрибьюторов
- Анализ покрытия устройств

## 🤝 Вклад в проект

### Добавление новых тестов

1. Создайте новый тестовый файл в `tests/`
2. Добавьте соответствующие Page Objects в `pages/`
3. Обновите `data/qr_payloads.py` для новых QR кодов
4. Добавьте команды в `Makefile.execution`

### Добавление новых устройств

1. Обновите `BROWSERSTACK_DEVICES` в `config/settings.py`
2. Добавьте параметризацию в тесты
3. Обновите команды Makefile

### Добавление новых дистрибьюторов

1. Добавьте QR код в `data/qr_payloads.py`
2. Обновите параметризацию тестов
3. Добавьте специфичные проверки

## 📞 Поддержка

### Полезные команды

```bash
# Полная очистка проекта
make clean

# Проверка конфигурации
make check-config

# Генерация QR кода для тестирования
make generate-qr

# Мониторинг BrowserStack
make monitor-browserstack
```

### Логи и отладка

- Логи сохраняются в `test.log`
- Скриншоты в `screenshots/`
- Отчеты в `reports/`
- BrowserStack сессии доступны в веб-интерфейсе

### Частые проблемы

1. **Ошибка подключения к BrowserStack**
   - Проверьте учетные данные в `.env`
   - Убедитесь в доступности устройств

2. **APK не загружается**
   - Проверьте размер файла (максимум 100MB)
   - Убедитесь в корректности APK

3. **Тесты падают на разных устройствах**
   - Проверьте локаторы элементов
   - Добавьте дополнительные ожидания

## 📚 Дополнительные ресурсы

- [BrowserStack App Automate Documentation](https://www.browserstack.com/app-automate)
- [Appium Documentation](http://appium.io/docs/en/about-appium/intro/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

---

**Автор:** Команда QA  
**Версия:** 1.0.0  
**Последнее обновление:** 2024
