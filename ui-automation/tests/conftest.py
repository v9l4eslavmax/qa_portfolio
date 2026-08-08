import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PASSWORD = "secret_sauce"

SCREENSHOTS_DIR = "screenshots"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Запускать браузер в headless-режиме (по умолчанию включено)",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат каждой фазы теста (setup/call/teardown) в item,
    чтобы фикстура driver ниже могла узнать, упал ли тест."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request):
    """Создаёт и возвращает WebDriver для каждого теста, закрывает после."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Снижаем "отпечаток" автоматизации — некоторые сайты с anti-bot защитой
    # (Cloudflare, DataDome и т.п.) распознают headless Selenium по этим
    # признакам и могут тихо блокировать часть действий без ошибки на
    # стороне драйвера.
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """
        },
    )
    drv.implicitly_wait(5)

    yield drv

    # Если тест упал — сохраняем скриншот для диагностики.
    # rep_call появляется в item благодаря хуку pytest_runtest_makereport выше.
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace(":", "_")
        drv.save_screenshot(os.path.join(SCREENSHOTS_DIR, f"{safe_name}.png"))

    drv.quit()


@pytest.fixture
def logged_in_page(driver):
    """Открывает сайт и авторизуется стандартным пользователем, возвращает driver."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)
    return driver
