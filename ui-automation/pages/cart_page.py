from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.utils import robust_click, wait_for_page_ready


class CartPage:
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_item_by_name(self, item_name: str):
        items = self.driver.find_elements(*self.CART_ITEMS)
        for item in items:
            if item_name in item.text:
                button = item.find_element(By.TAG_NAME, "button")
                self.wait.until(EC.element_to_be_clickable(button))
                robust_click(self.driver, button)
                # ждём, пока элемент реально исчезнет из DOM корзины
                self.wait.until(EC.staleness_of(item))
                return
        raise ValueError(f"Товар '{item_name}' не найден в корзине")

    def go_to_checkout(self):
        button = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        robust_click(self.driver, button)
        # дожидаемся реальной навигации на страницу checkout-step-one
        self.wait.until(EC.url_contains("checkout-step-one"))
        wait_for_page_ready(self.driver)


class CheckoutStepOnePage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        first_name_field = self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        first_name_field.send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        continue_button = self.driver.find_element(*self.CONTINUE_BUTTON)
        robust_click(self.driver, continue_button)

    def get_error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text


class CheckoutStepTwoPage:
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def finish(self):
        button = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        robust_click(self.driver, button)

    def get_total_text(self) -> str:
        return self.driver.find_element(*self.TOTAL_LABEL).text


class CheckoutCompletePage:
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def get_confirmation_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
