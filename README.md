# QA Portfolio — Максимов Вячеслав

Здесь собраны примеры ручного и автоматизированного тестирования: тест-планы, тест-кейсы, баг-репорты, API- и UI-автотесты с CI/CD.

## 🧰 Стек
- **Языки:** Python
- **Автоматизация UI:** Selenium WebDriver
- **Автоматизация API:** pytest + requests
- **CI/CD:** GitHub Actions
- **Отчётность:** Allure / pytest-html
- **Ручное тестирование:** тест-планы, чек-листы, баг-репорты

## 📁 Структура репозитория

| Папка | Что внутри |
|---|---|
| [`manual-testing/`](./manual-testing) | Тест-план, тест-кейсы, баг-репорты для тестового объекта |
| [`api-tests/`](./api-tests) | Автотесты API на pytest (reqres.in) |
| [`ui-automation/`](./ui-automation) | UI-автотесты на Selenium (saucedemo.com) |
| `.github/workflows/` | CI-пайплайн, автозапуск тестов при пуше |

## 🎯 Объекты тестирования
- **UI:** [SauceDemo](https://www.saucedemo.com/) — демо-магазин для тренировки автотестов
- **API:** [ReqRes](https://reqres.in/) — тестовое REST API

## 🚀 Как запустить тесты

### API-тесты
```bash
cd api-tests
pip install -r requirements.txt
pytest --html=report.html --self-contained-html
```

### UI-тесты
```bash
cd ui-automation
pip install -r requirements.txt
pytest --html=report.html --self-contained-html
```

## 📊 Результаты
Отчёты о последнем запуске тестов генерируются автоматически через GitHub Actions — см. вкладку **Actions**.



📧 [email](v9l4eslavmax@gmail.com) · 🔗 [LinkedIn](https://www.linkedin.com/in/viacheslav-maksimov-85b1293b7/) · 🔗 [Telegram](@MaksimovVyacheslav86)
