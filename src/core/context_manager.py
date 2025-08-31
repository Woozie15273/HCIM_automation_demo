from src.utils.driver_factory import DriverFactory

class WebDriverContextManager:
    def __init__(self, logger, headless=False):
        self.driver_factory = DriverFactory(logger, headless)

    def __enter__(self):
        self.driver = self.driver_factory.get_driver()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver_factory.quit_driver()
        if exc_type:
            # Optional: log the exception if needed
            self.driver_factory.logger.error(f"Exception in WebDriverContextManager: {exc_val}")

