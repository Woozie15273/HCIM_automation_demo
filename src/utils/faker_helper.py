from faker import Faker
import random
import string

from pandas import DataFrame

class fakeDataHelper:
    def __init__(self):
        self.faker = Faker("en_CA")

    def _get_file_name(self, for_HA: bool):
        if for_HA:
            self.file_name = "EmployeeInfo_All_HA_empty_PHN.xlsx"
        else:
            self.file_name = "EmployeeInfo_MS_Cactus_empty_PHN.xlsx"
        return self.file_name

    def _get_rowID(self):        
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=5))
        return f"{letters}-{digits}"

    def _get_last_name(self):
        return self.faker.last_name()
    
    def _get_first_name(self):
        return self.faker.first_name()
    
    def _get_dob(self):
        dob = self.faker.date_of_birth(minimum_age=18, maximum_age=90)
        return f"{dob.month}/{dob.day}/{dob.year}"
    
    def _get_post_code(self):
        return self.faker.postalcode()
    
    def _get_phone_number(self):        
        area = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line = random.randint(1000, 9999)
        return f"({area}) {prefix}-{line}"
    
    
    def _generate_entries(self, for_HA: bool, count: int) -> DataFrame:
        """Generate a DataFrame with `count` number of fake entries."""

        headers = {
            "HA_ROWID" if for_HA else "HA ROWID": self._get_rowID,
            "LAST NAME" if for_HA else "LASTNAME": self._get_last_name,
            "FIRST NAME" if for_HA else "FIRSTNAME": self._get_first_name,
            "DOB": self._get_dob,
            "POST CODE": self._get_post_code,
            "PHONE HOME" if for_HA else "MOBILE PHONE": self._get_phone_number
        }

        records = [
            {key: generator() for key, generator in headers.items()}
            for _ in range(count)
        ]

        return DataFrame(records)
    
    def sample_to_xlsx(self, for_HA: bool, count: int):
        file = self._get_file_name(for_HA)
        df = self._generate_entries(for_HA, count)
        df.to_excel(file, startrow = 1, index = False)

