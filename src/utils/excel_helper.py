import pandas as pd
from pathlib import Path

class ExcelHelper:
    def __init__(self, logger):
        self.logger = logger
    
    def to_Excel(self, data_frame: pd.DataFrame, path: str) -> None:
            try:
                data_frame.to_excel(path, index=False)
                self.logger.info("DataFrame written to Excel: %s", path)
            except Exception as e:
                self.logger.error("Failed to write DataFrame to Excel: %s", e)

    def get_data_from(self, path: str):
        self.logger.info("Reading Excel file: %s", path)
        try:
            personal_information = pd.read_excel(path, header=1)
            print(personal_information)
            self.logger.debug("Excel file read successfully with shape: %s", personal_information.shape)

            if "All_HA" in str(path):
                return self._all_HA_helper(personal_information)
            else:
                return self._MS_Catus_helper(personal_information)
        except Exception as e:
            self.logger.error("Failed to read or process Excel file: %s", e)
            return pd.DataFrame()  # Return empty DataFrame on failure

    def _all_HA_helper(self, data_frame: pd.DataFrame):
        self.logger.debug("Processing All_HA format")
        data_frame = data_frame.filter(["HA_ROWID", "LAST NAME", "FIRST NAME", "DOB", "POST CODE", "PHONE HOME"])
        return self._dob_helper(data_frame)

    def _MS_Catus_helper(self, data_frame: pd.DataFrame):
        self.logger.debug("Processing MS_Catus format")
        data_frame = data_frame.filter(["HA ROWID", "LASTNAME", "FIRSTNAME", "DOB", "POST CODE", "MOBILE PHONE"]).dropna()
        data_frame.columns = ["HA_ROWID", "LAST NAME", "FIRST NAME", "DOB", "POST CODE", "PHONE HOME"]
        return self._dob_helper(data_frame)

    def _dob_helper(self, data_frame: pd.DataFrame):
        self.logger.debug("Normalizing DOB format")
        try:
            data_frame["DOB"] = pd.to_datetime(data_frame["DOB"])
            data_frame["DOB"] = data_frame["DOB"].dt.strftime('%Y-%b-%d')
            return data_frame
        except Exception as e:
            self.logger.error("Failed to normalize DOB: %s", e)
            return data_frame

    def generate_comparable_copy(self, data_frame: pd.DataFrame, path: str):
        self.logger.info("Generating comparable copy to: %s", path)
        try:
            phn_lookup = data_frame.copy()
            phn_lookup.insert(3, "PHN", "")
            phn_lookup = phn_lookup[["HA_ROWID", "LAST NAME", "FIRST NAME", "PHN", "DOB"]]
            phn_lookup.columns = ["HA_ROWID", "Last Name", "First Name", "PHN", "Date of Birth"]
            output_path = Path(path) / "PHN_Lookup.xlsx"
            self.to_Excel(phn_lookup, str(output_path))
        except Exception as e:
            self.logger.error("Failed to generate comparable copy: %s", e)

    def generate_output(self, data_frame: pd.DataFrame, path: str):        
        try:
            self.logger.info("Generating final output to: %s", path)
            data_frame[["Last Name", "First Name"]] = data_frame["Name"].str.split(",", n=1, expand=True)
            data_frame = data_frame[["Last Name", "First Name", "Address", "Telephone", "PHN", "Date of Birth", "Date of Death", "Gender", "Score"]]
            output_path = Path(path) / "PHN_Results.xlsx"
            self.to_Excel(data_frame, str(output_path))            
        
        except ValueError as ve:
            if "Columns must be same length as key" in str(ve):
                self.logger.error("No matching PHN from given data")
            else:
                self.logger.error("ValueError occurred: %s", ve)

        except Exception as e:
            self.logger.error("Failed to generate output: %s", e)


    def extract_high_score_phns_from_html(self, row_data_list, df_to_append):
        """
        Appends a list of row data (each a list of <td> values) to an existing DataFrame.

        Parameters:
        - row_data_list: list of lists, where each inner list represents a row of cell values
        - df_to_append: existing DataFrame to append results to

        Returns:
        - Updated DataFrame with new rows appended
        """
        try:
            if not row_data_list:
                self.logger.info("No rows to process.")
                return df_to_append

            # Convert to DataFrame with specified columns
            new_df = pd.DataFrame(row_data_list, columns = ["Name", "Address", "Telephone", "PHN", "Date of Birth", "Date of Death", "Gender", "Score"])

            # Convert Score column to numeric
            new_df["Score"] = pd.to_numeric(new_df["Score"], errors="coerce")

            # Append to existing DataFrame
            df_to_append = pd.concat([df_to_append, new_df], ignore_index=True)

        except Exception as e:
            self.logger.error(f"Error processing row data: {e}")

        return df_to_append
    
    def initiate_new_df(self):
        """
        Initializes an empty DataFrame with predefined columns and data types.

        Returns:
            pd.DataFrame: An empty DataFrame with specified column names and types.
        """
        return pd.DataFrame({
            "Name": pd.Series(dtype="str"),
            "Address": pd.Series(dtype="str"),
            "Phone": pd.Series(dtype="str"),
            "PHN": pd.Series(dtype="int64"),
            "DOB": pd.Series(dtype="str"),
            "Unknown": pd.Series(dtype="str"),
            "Gender": pd.Series(dtype="str"),
            "Score": pd.Series(dtype="float")
        })