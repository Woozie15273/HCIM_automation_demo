from tqdm import tqdm
from .config_loader import ConfigLoader
from .context_manager import WebDriverContextManager
from .logger import setup_logger
from src.pages.login_page import LoginPage
from src.pages.search_page import SearchPage
from src.utils.excel_helper import ExcelHelper

class MainApp:
    def __init__(self):        
        self.config = ConfigLoader()
        self.config.load()
        self.config.print_config()
        self.logger = setup_logger("app", enable_log = self.config.enable_log)
        self.driver_context = WebDriverContextManager(logger = self.logger, headless = self.config.headless)
        self.driver = self.driver_context.__enter__()
        self.login = LoginPage(logger = self.logger, driver = self.driver, config = self.config)
        self.search = SearchPage(logger = self.logger, driver = self.driver)
        self.excel = ExcelHelper(logger = self.logger)

    def teardown(self):
        self.driver_context.__exit__(None, None, None)

    def run(self):        
        personal_info = self.excel.get_data_from(self.config.all_ha_xlsx) if self.config.search_all_ha else self.excel.get_data_from(self.config.ms_cactus_xlsx)
        
        self.excel.generate_comparable_copy(personal_info, self.config.source_folder)

        personal_info_clip = self._get_slice_from_index(personal_info, self.config.search_index)
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

    def _get_slice_from_index(self, dataframe, Search_Index):
        """
        Returns a slice of the DataFrame based on the Search_Index input.

        Parameters:
            dataframe (pd.DataFrame): The DataFrame to slice.
            Search_Index (list or slice): Either a list of 0 to 3 elements [start, stop, step],
                                        or a slice object.

        Returns:
            pd.DataFrame: The sliced DataFrame.
        """
        if Search_Index is None:
            return dataframe  # Return full DataFrame if None

        if isinstance(Search_Index, slice):
            return dataframe[Search_Index]

        if isinstance(Search_Index, list):
            if len(Search_Index) > 3:
                raise ValueError("Search_Index should be a list of 0 to 3 elements (start, stop, step).")
            return dataframe[slice(*Search_Index)]

        raise TypeError("Search_Index must be either a list or a slice object.")