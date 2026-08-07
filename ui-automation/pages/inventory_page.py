from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self) -> bool:
        return self.driver.current_url == self.URL

    def add_item_to_cart_by_name(self, item_name: str):
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        for item in items:
            if item_name in item.text:
                item.find_element(By.TAG_NAME, "button").click()
                return
        raise ValueError(f"Товар '{item_name}' не найден в каталоге")

    def get_cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        if not badges:
            return 0
        return int(badges[0].text)

    def open_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def sort_by(self, option_label: str):
        dropdown = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        dropdown.select_by_visible_text(option_label)

    def get_prices(self) -> list[float]:
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(e.text.replace("$", "")) for e in elements]
