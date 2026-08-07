from selenium.webdriver.common.by import By


class CartPage:
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    def get_items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def remove_item_by_name(self, item_name: str):
        items = self.driver.find_elements(*self.CART_ITEMS)
        for item in items:
            if item_name in item.text:
                item.find_element(By.TAG_NAME, "button").click()
                return
        raise ValueError(f"Товар '{item_name}' не найден в корзине")

    def go_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()


class CheckoutStepOnePage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_error_text(self) -> str:
        return self.driver.find_element(*self.ERROR_MESSAGE).text


class CheckoutStepTwoPage:
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver):
        self.driver = driver

    def finish(self):
        self.driver.find_element(*self.FINISH_BUTTON).click()

    def get_total_text(self) -> str:
        return self.driver.find_element(*self.TOTAL_LABEL).text


class CheckoutCompletePage:
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver

    def get_confirmation_text(self) -> str:
        return self.driver.find_element(*self.COMPLETE_HEADER).text
