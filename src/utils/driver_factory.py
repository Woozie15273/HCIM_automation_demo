from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

class DriverFactory:
    def __init__(self, logger, headless=False):
        self.logger = logger
        self.headless = headless
        self.driver = None        

    def get_driver(self):
        self.logger.info("Creating WebDriver instance")
        try:
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")

            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(10)
            self.logger.info("WebDriver successfully created")
            return self.driver
        except Exception as e:
            self.logger.error("Failed to create WebDriver: %s", e)
            raise

    def quit_driver(self):
        if self.driver:
            self.logger.info("Quitting WebDriver")
            self.driver.quit()
