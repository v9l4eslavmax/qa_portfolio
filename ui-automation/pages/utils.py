import time
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains


def robust_click(driver, element):
    """
    Кликает по элементу максимально надёжно.

    Обычный element.click() в headless Chrome на CI иногда не долетает до
    обработчика события сайта — элемент физически на странице и формально
    "кликабелен", но JS-обработчик мог ещё не навесится в момент клика,
    либо клик по координатам не совпадает с отрисованным местом из-за
    задержек рендера на медленном раннере.

    Пробуем по нарастающей: обычный клик -> клик через ActionChains
    (реальные синтетические события мыши через W3C Actions API,
    надёжнее для "капризных" элементов) -> клик через JS напрямую по
    DOM-узлу как последний резерв.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.2)  # даём странице "устояться" после скролла

    try:
        element.click()
        return
    except (ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException):
        pass

    try:
        ActionChains(driver).move_to_element(element).pause(0.1).click().perform()
        return
    except Exception:
        pass

    driver.execute_script("arguments[0].click();", element)


def wait_for_page_ready(driver, timeout=10):
    """Ждёт, пока document.readyState станет 'complete' — полезно после
    кликов, вызывающих переход на новую страницу."""
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # Небольшая пауза сверх readyState: на некоторых SPA-сайтах JS
    # навешивает обработчики событий чуть позже, чем документ считается
    # "готовым" — это защита от гонки между рендером и биндингом событий.
    time.sleep(0.3)
