import unittest

from src.core.config_loader import ConfigLoader

class TestConfigLoaderWithIni(unittest.TestCase):
    def test_config_loader_reads_ini(self):
        loader = ConfigLoader()
        loader.load()
        loader.print_config()

if __name__ == '__main__':
    unittest.main()
