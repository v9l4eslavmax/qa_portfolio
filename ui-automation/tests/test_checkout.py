from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage, CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


class TestCheckout:
    def test_full_checkout_flow_e2e(self, logged_in_page):
        """
        E2E-сценарий: логин -> добавление товара -> корзина ->
        оформление заказа -> подтверждение.
        """
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(logged_in_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(logged_in_page)
        checkout_step_one.fill_info("John", "Doe", "12345")

        checkout_step_two = CheckoutStepTwoPage(logged_in_page)
        checkout_step_two.finish()

        checkout_complete = CheckoutCompletePage(logged_in_page)
        assert "thank you" in checkout_complete.get_confirmation_text().lower()

    def test_checkout_fails_without_first_name(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(logged_in_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(logged_in_page)
        checkout_step_one.fill_info("", "Doe", "12345")

        assert "first name is required" in checkout_step_one.get_error_text().lower()
