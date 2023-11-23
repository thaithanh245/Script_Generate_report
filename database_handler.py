import json
import os

class DatabaseHandler:

    def __init__(self, database_dir:str):
        self.database_dir = database_dir
        self.SWTS_DOORS_FILE_NAME = "SWTS_DOORS.json"
        self.TRS_DOORS_FILE_NAME = "TRS_DOORS.json"
        self.REQ_COVERAGE_FILE_NAME = "REQ_COVERAGE.json"
        # self.load_html_file_database()
        # self.load_test_cases_result_database()

    def save_SWTS_DOORS_database(self, database:dict):
        """
        @Description: save input database to obj attribute and output an json file of the database
        @Input: database dict
        """
        self.SWTS_DOORS_database = database
        database_dict = json.dumps(database, indent=4)
        with open (f"{self.database_dir}\\{self.SWTS_DOORS_FILE_NAME}", "w") as database_file:
            database_file.write(database_dict)

    def save_TRS_DOORS_database(self, database:dict):
        """
        @Description: save input database to obj attribute and output an json file of the database
        @Input: database dict
        """
        self.TRS_DOORS_database = database
        database_dict = json.dumps(database, indent=4)
        with open (f"{self.database_dir}\\{self.TRS_DOORS_FILE_NAME}", "w") as database_file:
            database_file.write(database_dict)

    def save_req_coverage_database(self, database:dict):
        """
        @Description: save input database to obj attribute and output an json file of the database
        @Input: database dict
        """
        self.req_coverage_database = database
        database_dict = json.dumps(database, indent=4)
        with open (f"{self.database_dir}\\{self.REQ_COVERAGE_FILE_NAME}", "w") as database_file:
            database_file.write(database_dict)
        
    
    def load_SWTS_DOORS_database(self):
        """
        @Description: load json file database to obj attribute and output an json file of the database
        @Input: None
        """
        if os.path.isfile(f"{self.database_dir}\\{self.SWTS_DOORS_FILE_NAME}") == True:
            with open (f"{self.database_dir}\\{self.SWTS_DOORS_FILE_NAME}", "r") as database_file:
                database = json.load(database_file)
            self.html_file_name_database = database
        else:
            print(f"file '{self.database_dir}\\{self.SWTS_DOORS_FILE_NAME}' not exist!")
            print(f"creating new {self.SWTS_DOORS_FILE_NAME}...")
            empty_database = {}
            self.save_SWTS_DOORS_database(database=empty_database)

    def load_TRS_DOORS_database(self):
        """
        @Description: load json file database to obj attribute and output an json file of the database
        @Input: None
        """
        if os.path.isfile(f"{self.database_dir}\\{self.TRS_DOORS_FILE_NAME}") == True:
            with open (f"{self.database_dir}\\{self.TRS_DOORS_FILE_NAME}", "r") as database_file:
                database = json.load(database_file)
            self.test_result_database = database
        else:
            print(f"file '{self.database_dir}\\{self.TRS_DOORS_FILE_NAME}' not exist!")
            print(f"creating new {self.TRS_DOORS_FILE_NAME}...")
            empty_database = {}
            self.save_TRS_DOORS_database(database=empty_database)

    def load_req_coverage_database(self):
        """
        @Description: load json file database to obj attribute and output an json file of the database
        @Input: None
        """
        if os.path.isfile(f"{self.database_dir}\\{self.REQ_COVERAGE_FILE_NAME}") == True:
            with open (f"{self.database_dir}\\{self.REQ_COVERAGE_FILE_NAME}", "r") as database_file:
                database = json.load(database_file)
            self.test_result_database = database
        else:
            print(f"file '{self.database_dir}\\{self.REQ_COVERAGE_FILE_NAME}' not exist!")
            print(f"creating new {self.REQ_COVERAGE_FILE_NAME}...")
            empty_database = {}
            self.save_req_coverage_database(database=empty_database)

    # def get_test_result(self):
    #     """
    #     @Return: a dict contain all test result of test cases extracted from html report
    #     """
    #     return self.all_variant_VT_sys_ch_database
