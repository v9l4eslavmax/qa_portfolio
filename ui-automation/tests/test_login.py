import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:
    def test_successful_login_with_standard_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()

    def test_login_with_locked_out_user_shows_error(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")

        assert "locked out" in login_page.get_error_text().lower()

    def test_login_with_wrong_password_shows_error(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "wrong_password")

        assert "do not match" in login_page.get_error_text().lower()

    def test_login_with_empty_username_shows_error(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "secret_sauce")

        assert "username is required" in login_page.get_error_text().lower()

    @pytest.mark.parametrize("username", [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
    ])
    def test_login_succeeds_for_valid_users(self, driver, username):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(username, "secret_sauce")

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
