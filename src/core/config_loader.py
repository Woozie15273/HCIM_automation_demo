import configparser
from pathlib import Path
import sys

from .logger import setup_logger  # Use relative import since it's in the same package

class ConfigLoader:
    """
    Load configuration from config.ini within the same folder.
    """
    def __init__(self, config_file="config.ini"):
        if getattr(sys, 'frozen', False):
            # Running as a bundled executable
            self.base_path = Path(sys.executable).resolve().parent
        else:
            # Running in a normal Python environment
            self.base_path = Path(__file__).resolve().parent.parent.parent

        self.config_path = self.base_path / config_file
        self.config = configparser.ConfigParser()        

    def load(self):             
        self.config.read(self.config_path)
        self.enable_log = self.config.getboolean('Flags', 'enable_log')
        self.logger = setup_logger("app", enable_log=self.enable_log)

        self.logger.info("Loading configuration...")

        try:
            self.source_folder = self.base_path / self.config['Paths']['source_folder']
            self.output_folder = self.base_path / self.config['Paths']['output_folder']

            self.all_ha_xlsx = next(self.source_folder.glob(self.config['Files']['all_ha_xlsx_pattern']), None)
            self.ms_cactus_xlsx = next(self.source_folder.glob(self.config['Files']['ms_cactus_xlsx_pattern']), None)

            self.username = self.config['Credentials']['username']
            self.password = self.config['Credentials']['password']

            self.search_all_ha = self.config.getboolean('Flags', 'search_all_ha')
            self.on_ha_network = self.config.getboolean('Flags', 'on_ha_network')
            self.headless = self.config.getboolean('Flags', 'headless')

            self.hcim_login = self.config['URLs']['hcim_login']
            self.hcim_home = self.config['URLs']['hcim_home']
            self.hcim_search = self.config['URLs']['hcim_search']

            raw_slice = self.config['Search']['search_index']
            self.search_index = self._parse_slice(raw_slice)

            self.logger.info("Configuration loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _parse_slice(self, slice_str):
        """
        Helper method to convert search_index from .ini to a python-readable format
        """
        slice_str = slice_str.strip("[]")
        parts = slice_str.split(":")
        start = int(parts[0]) if parts[0] else None
        end = int(parts[1]) if len(parts) > 1 and parts[1] else None
        return slice(start, end)
    
    def print_config(self):
        self.logger.info("Current Configuration:")
        self.logger.info(f"Resolved config path: {self.config_path}")
        self.logger.info(f"Source Folder: {self.source_folder}")
        self.logger.info(f"Output Folder: {self.output_folder}")
        self.logger.info(f"All HA XLSX: {self.all_ha_xlsx}")
        self.logger.info(f"MS Cactus XLSX: {self.ms_cactus_xlsx}")
        self.logger.info(f"Username: {self.username}")
        self.logger.info(f"Password: {self.password}")
        self.logger.info(f"Search All HA: {self.search_all_ha}")
        self.logger.info(f"On HA Network: {self.on_ha_network}")
        self.logger.info(f"Enable Log: {self.enable_log}")
        self.logger.info(f"Headless: {self.headless}")
        self.logger.info(f"Search Index: {self.search_index}")
