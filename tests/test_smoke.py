import unittest

from src.core.logger import setup_logger
from src.core.config_loader import ConfigLoader
from src.core.context_manager import WebDriverContextManager
from src.pages.login_page import LoginPage
from src.pages.search_page import SearchPage
from src.utils.excel_helper import ExcelHelper

from tqdm import tqdm
from pandas import DataFrame

class TestEndtoEnd(unittest.TestCase):
    def setUp(self):
        self.config = ConfigLoader()
        self.config.load()
        self.logger = setup_logger("app", enable_log = self.config.enable_log)
        self.driver_context = WebDriverContextManager(logger = self.logger, headless = self.config.headless)
        self.driver = self.driver_context.__enter__()
        self.login = LoginPage(logger = self.logger, driver = self.driver, config = self.config)
        self.search = SearchPage(logger = self.logger, driver = self.driver)
        self.excel = ExcelHelper(logger = self.logger)

    def tearDown(self):
        self.driver_context.__exit__(None, None, None)

    def test_smoke_HA(self):
        personal_info = self.excel.get_data_from(self.config.all_ha_xlsx)
        self._helper_smoke(personal_info)
        
    
    def test_smoke_MS(self):
        personal_info = self.excel.get_data_from(self.config.ms_cactus_xlsx)      
        self._helper_smoke(personal_info)  

    
    def _helper_smoke(self, personal_info: DataFrame):
        self.excel.generate_comparable_copy(personal_info, self.config.output_folder)

        personal_info_clip = personal_info[:5]
        PHN_Results = self.excel.initiate_new_df()

        self.login.login()

        for item, row in tqdm(personal_info_clip.iterrows(), total=personal_info_clip.shape[0]):
            try:
                self.search.perform_search(row)

                qualified_entries = self.search.trim_result()
                PHN_Results = self.excel.extract_high_score_phns_from_html(qualified_entries, PHN_Results)

                self.search.clear_form()
                
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                self.excel.generate_output(PHN_Results, self.config.output_folder)
                break

        self.excel.generate_output(PHN_Results, self.config.output_folder)