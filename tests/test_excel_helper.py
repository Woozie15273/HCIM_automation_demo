import unittest

from src.core.logger import setup_logger
from src.utils.excel_helper import ExcelHelper
from src.core.config_loader import ConfigLoader
from src.utils.faker_helper import fakeDataHelper

class TestExcels(unittest.TestCase):
    def setUp(self):
        self.config = ConfigLoader()
        self.config.load()
        self.config.print_config()
        self.logger = setup_logger("app", enable_log = self.config.enable_log)
        self.faker = fakeDataHelper()
        self.logger.info("Setting up Excel Helper instance.")
        self.excel = ExcelHelper(logger = self.logger)       

    def test_generate_fake_demo_data_HA(self):
        self.logger.info("Running test: test_generate_fake_demo_data_HA")
        self.faker.sample_to_xlsx(True, 5)        

    def test_generate_fake_demo_data_MS(self):
        self.logger.info("Running test: test_generate_fake_demo_data_MS")
        self.faker.sample_to_xlsx(False, 5)
        
    def test_prepare_HA_data_for_search(self):
        self.logger.info("Running test: test_prepare_HA_data_for_search")
        personal_info = self.excel.get_data_from(self.config.all_ha_xlsx)
        self.logger.info(f"Retrieved HA data: {personal_info}")

    def test_prepare_MS_data_for_search(self):
        self.logger.info("Running test: test_prepare_MS_data_for_search")
        personal_info = self.excel.get_data_from(self.config.ms_cactus_xlsx)
        self.logger.info(f"Retrieved MS data: {personal_info}")

    def test_generate_comparable_copy_HA(self):
        self.logger.info("Running test: test_generate_comparable_copy_HA")
        personal_info_HA = self.excel.get_data_from(self.config.all_ha_xlsx)
        self.logger.info("Retrieved HA data with shape: %s", personal_info_HA.shape)
        self.excel.generate_comparable_copy(personal_info_HA, self.config.output_folder)
        self.logger.info("Comparable copy for HA data generated successfully.")

    def test_generate_comparable_copy_MS(self):
        self.logger.info("Running test: test_generate_comparable_copy_MS")
        personal_info_MS = self.excel.get_data_from(self.config.ms_cactus_xlsx)
        self.logger.info("Retrieved MS data with shape: %s", personal_info_MS.shape)
        self.excel.generate_comparable_copy(personal_info_MS, self.config.output_folder)
        self.logger.info("Comparable copy for MS data generated successfully.")

if __name__ == '__main__':
    unittest.main()

    
    

