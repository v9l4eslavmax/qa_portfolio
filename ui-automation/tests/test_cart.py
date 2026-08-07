from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:
    def test_add_single_item_to_cart(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")

        assert inventory_page.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")

        assert inventory_page.get_cart_count() == 2

    def test_cart_is_empty_by_default(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        assert inventory_page.get_cart_count() == 0

    def test_remove_item_from_cart(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(logged_in_page)
        assert cart_page.get_items_count() == 1

        cart_page.remove_item_by_name("Sauce Labs Backpack")
        assert cart_page.get_items_count() == 0

    def test_sort_items_by_price_low_to_high(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.sort_by("Price (low to high)")

        prices = inventory_page.get_prices()
        assert prices == sorted(prices)
