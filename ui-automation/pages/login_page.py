from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.utils import robust_click


class LoginPage:
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))

    def login(self, username: str, password: str):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        robust_click(self.driver, login_button)

    def get_error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
