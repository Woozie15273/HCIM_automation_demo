from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, logger, driver, timeout=10):
        self.logger = logger
        self.driver = driver
        self.timeout = timeout
        logger.info("BasePage initialized with timeout=%s", timeout)

    def get(self, url: str):
        self.logger.info("Navigating to URL: %s", url)
        self.driver.get(url)

    def find_element_by_id(self, element_id):
        self.logger.debug("Finding element by ID: %s", element_id)
        return self.driver.find_element(By.ID, element_id)

    def wait_until(self, expected_condition):
        self.logger.debug("Waiting for expected condition: %s", expected_condition)
        return WebDriverWait(self.driver, self.timeout).until(expected_condition)

    def wait_for_element(self, by, value):
        self.logger.info("Waiting for element by %s with value: %s", by, value)
        return self.wait_until(EC.presence_of_element_located((by, value)))    
    
    def wait_for_element_invisible_by_id(self, element_id):
        self.logger.info("Waiting for element with ID '%s' to become invisible", element_id)
        return self.wait_until(EC.invisibility_of_element_located((By.ID, element_id)))

    def click(self, element):
        self.logger.debug("Clicking on element: %s", element)
        element.click()

    def clear(self, element):
        self.logger.debug("Clearing element: %s", element)
        element.clear()

    def send_keys(self, element, keys):
        self.logger.debug("Sending keys to element: %s", element)
        element.send_keys(keys)