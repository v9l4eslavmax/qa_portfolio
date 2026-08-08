from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)


def robust_click(driver, element):
    """
    Кликает по элементу максимально надёжно.

    В headless Chrome на CI обычный element.click() иногда "не долетает" —
    клик идёт по координатам и может быть перехвачен наложенным элементом
    (sticky-шапка, баннер, невидимый оверлей), из-за чего действие сайта
    не срабатывает, хотя Selenium не бросает исключение.

    Сначала прокручиваем элемент в центр видимой области, пробуем обычный
    клик; если он перехвачен или элемент временно неинтерактивен —
    кликаем через JS напрямую по DOM-элементу, что не зависит от координат
    и перехвата.
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException):
        driver.execute_script("arguments[0].click();", element)


def wait_for_page_ready(driver, timeout=10):
    """Ждёт, пока document.readyState станет 'complete' — полезно после
    кликов, вызывающих переход на новую страницу."""
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
