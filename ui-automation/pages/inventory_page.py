from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.utils import robust_click, wait_for_page_ready
import time


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def is_loaded(self) -> bool:
        self.wait.until(EC.url_to_be(self.URL))
        wait_for_page_ready(self.driver)
        return self.driver.current_url == self.URL

    def add_item_to_cart_by_name(self, item_name: str):
        self.wait.until(EC.presence_of_element_located(self.INVENTORY_ITEMS))
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        for item in items:
            if item_name in item.text:
                button = item.find_element(By.TAG_NAME, "button")
                self.wait.until(EC.element_to_be_clickable(button))
                robust_click(self.driver, button)
                # ждём, пока кнопка реально сменится на "Remove" —
                # подтверждение, что клик подействовал, а не просто прошёл мимо
                self.wait.until(
                    lambda d: "Remove" in item.find_element(By.TAG_NAME, "button").text
                )
                time.sleep(0.3)  # даём странице "устояться" перед следующим действием
                return
        raise ValueError(f"Товар '{item_name}' не найден в каталоге")

    def get_cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        if not badges:
            return 0
        return int(badges[0].text)

    def open_cart(self):
        cart_link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        robust_click(self.driver, cart_link)
        self.wait.until(EC.url_contains("cart.html"))
        wait_for_page_ready(self.driver)

    def sort_by(self, option_label: str):
        dropdown_element = self.wait.until(EC.presence_of_element_located(self.SORT_DROPDOWN))
        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text(option_label)

    def get_prices(self) -> list[float]:
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(e.text.replace("$", "")) for e in elements]
