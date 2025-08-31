from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pandas import Series
from time import sleep

from .base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, logger ,driver, timeout=5):
        super().__init__(logger, driver)
        self.timeout = timeout
        self.logger = logger
        logger.info("SearchPage initialized with timeout=%s", timeout)

    @property
    def input_surname(self):
        return self.find_element_by_id("fcSearchByOtherForm:surname")

    @property
    def input_firstname(self):
        return self.find_element_by_id("fcSearchByOtherForm:firstName")

    @property
    def input_dob(self):
        return self.find_element_by_id("fcSearchByOtherForm:dateOfBirth_input")

    @property
    def input_tel(self):
        return self.find_element_by_id("fcSearchByOtherForm:telephone")

    @property
    def input_pos(self):
        return self.find_element_by_id("fcSearchByOtherForm:postalCode")

    @property
    def search_btn(self):
        return self.find_element_by_id("fcSearchByOtherForm:searchBtn")

    @property
    def e_table(self):
        return self.wait_for_element(By.ID, "fcSearchByOtherForm:candidatesTable_data")
    
  
    def perform_search(self, search_row: Series):
        """
        Performs a search operation using data from a pandas Series (a DataFrame row).

        Args:
            search_row (pd.Series): A pandas Series representing a row from a DataFrame,
                                     containing 'LAST NAME', 'FIRST NAME', "DOB", 'PHONE HOME', and 'POST CODE'.
        """

        self.logger.info("Performing search with data: %s", search_row.to_dict())
        try:
            self.send_keys(self.input_surname, search_row["LAST NAME"])
            self.send_keys(self.input_firstname, search_row["FIRST NAME"])
            self.send_keys(self.input_dob, search_row["DOB"])
            self.send_keys(self.input_tel, search_row["PHONE HOME"])
            self.send_keys(self.input_pos, search_row["POST CODE"])
            self._time_sleep()
            self.click(self.search_btn)
            self.wait_for_element_invisible_by_id("j_idt40_modal")
            self.logger.info("Search submitted successfully")
        except Exception as e:
            self.logger.error("Search failed: %s", e)

    def _time_sleep(self):
        self.logger.debug("Sleeping for %s seconds before search", self.timeout)
        sleep(self.timeout)

    def clear_form(self):
        self.logger.info("Clearing search form")
        try:
            self.clear(self.input_surname)
            self.clear(self.input_firstname)
            self.clear(self.input_tel)
            self.clear(self.input_pos)
            self._clear_calendar(self.input_dob)
            self.logger.debug("Form cleared successfully")
        except Exception as e:
            self.logger.error("Failed to clear form: %s", e)

    def _clear_calendar(self, element):
        self.logger.debug("Clearing calendar input")        
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
        
    def trim_result(self):
        self.logger.info("Trimming search results with score >= 10")
        try:
            table = self.e_table
            rows = table.find_elements(By.TAG_NAME, "tr")
            matching_data = []

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    score_text = cells[-1].get_attribute("innerText").strip()
                    try:
                        score = float(score_text)
                        if score >= 10:
                            row_data = [cell.get_attribute("innerText").strip() for cell in cells]
                            self.logger.info(row_data)
                            matching_data.append(row_data)
                            
                    except ValueError:
                        self.logger.warning("Skipping row with non-numeric score: %s", score_text)

            self.logger.info("Found %d matching rows", len(matching_data))
            return matching_data

        except Exception as e:
            self.logger.error("Error while trimming results: %s", e)
            return matching_data