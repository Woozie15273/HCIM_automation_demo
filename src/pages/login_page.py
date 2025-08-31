from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage
from src.core.config_loader import ConfigLoader

class LoginPage(BasePage):
    def __init__(self, logger, driver, config):
        super().__init__(logger, driver)
        self.config = config
        self.logger = logger
        logger.info("LoginPage initialized")

    def login(self):
        if self.config.on_ha_network:
            self.login_network()
        else:
            self.login_public()

    def login_network(self):
        self.logger.info("Attempting network login (PHSA)")
        try:
            self._login_helper()
            self._call_back_handler()
            self.logger.info("Network login successful")
        except Exception as e:
            self.logger.error("Network login failed: %s", e)

    def login_public(self):
        self.logger.info("Attempting public login with username: %s", self.config.username)
        try:
            self._login_helper()
            self.send_keys(self.wait_for_element(By.ID, "userNameInput"), self.config.username)
            self.send_keys(self.find_element_by_id("passwordInput"), self.config.password)
            self.click(self.find_element_by_id("submitButton"))
            self._call_back_handler()
            self.logger.info("Public login successful")
        except Exception as e:
            self.logger.error("Public login failed: %s", e)

    def _login_helper(self):
        self.logger.debug("Navigating to login page and clicking PHSA login")
        self.get(self.config.hcim_login)
        self.click(self.wait_for_element(By.ID, "zocial-phsa"))

    def _call_back_handler(self):
        self.logger.debug("Handling login callback")
        self.wait_until(EC.any_of(
            EC.url_contains("callback"),
            EC.url_contains("home")
        ))

        current_url = self.driver.current_url
        self.logger.debug("Current URL after login: %s", current_url)

        if "callback" in current_url:
            self.logger.info("Detected callback URL, redirecting to home and search")
            self.get(self.config.hcim_home)
            self.get(self.config.hcim_search)
        else:
            self.logger.info("Directly navigating to search page")
            self.get(self.config.hcim_search)