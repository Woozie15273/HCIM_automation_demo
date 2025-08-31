import unittest

from pandas import Series
from src.core.logger import setup_logger
from src.core.config_loader import ConfigLoader
from src.core.context_manager import WebDriverContextManager
from src.pages.login_page import LoginPage
from src.pages.search_page import SearchPage


class TestHCIM(unittest.TestCase):
    
    def setUp(self):
        self.config = ConfigLoader()
        self.config.load()
        self.logger = setup_logger("app", enable_log = self.config.enable_log)
        self.driver_context = WebDriverContextManager(logger = self.logger, headless = self.config.headless)
        self.driver = self.driver_context.__enter__()
        self.login = LoginPage(logger = self.logger, driver = self.driver, config = self.config)
        self.search = SearchPage(logger = self.logger, driver = self.driver)

    def tearDown(self):
        self.logger.info("Tearing down Selenium context.")
        self.driver_context.__exit__(None, None, None)  

    def test_login_network(self):
        self.logger.info("Running test: test_login_network")
        self.login.login_network()
        current_url = self.driver.current_url
        self.logger.info(f"Current URL after login_network: {current_url}")
        self.assertIn(self.config.hcim_search, current_url)

    def test_login_public(self):
        self.logger.info("Running test: test_login_public")
        self.login.login_public()
        current_url = self.driver.current_url
        self.logger.info(f"Current URL after login_public: {current_url}")
        self.assertIn(self.config.hcim_search, current_url)

    def test_search_and_clear(self):        
        self.logger.info("Running test: test_search_and_clear")
        local = Series({
            "LAST NAME": "Wu",
            "FIRST NAME": "Ziping",
            "DOB": "1997-Jul-06",
            "PHONE HOME": "", 
            "POST CODE": ""
        })
        self.login.login()
        self.logger.info("Performing search with provided data.")
        self.search.perform_search(local)
        matching_rows = self.search.trim_result()
        self.logger.info(f"Found {len(matching_rows)} matching rows.")
        self.search.clear_form()

if __name__ == '__main__':
    unittest.main()
