import json
import os
import shutil

class ConfigHandler:
    def __int__(self):
        self.all_config = {}

    def load_config(self):
        cwd = os.getcwd() + "\\"

        with open("Config.json", "r") as config_file:
            self.all_config = json.load(config_file)
        for key in self.all_config["file_dir"].keys():
            self.all_config["file_dir"][key] = cwd + self.all_config["file_dir"][key]

    def clean_up_and_reset_output(self):
        output_folder_dir = self.all_config["file_dir"]["output"]
        database_folder_dir = self.all_config["file_dir"]["database"]
        # delete and create new output folder
        if os.path.isdir(output_folder_dir) == True:
            shutil.rmtree(output_folder_dir)
        os.mkdir(output_folder_dir)
        # if Database folder got deleted, create new Database folder
        if os.path.isdir(database_folder_dir) != True:
            os.mkdir(database_folder_dir)
    
    def get_excel_template_test_report(self):
        return self.all_config["file_dir"]["excel_template_test_report"]
    
    def get_excel_TRS_DOORS(self):
        return self.all_config["file_dir"]["excel_TRS_DOORS"]
    
    def get_excel_SWTS_DOORS(self):
        return self.all_config["file_dir"]["excel_SWTS_DOORS"]
    
    def get_database_folder(self):
        return self.all_config["file_dir"]["database"]
    
    def get_output_folder(self):
        return self.all_config["file_dir"]["output"]
    
    def get_excel_test_report_output(self):
        return self.all_config["file_dir"]["excel_test_report_output"]
        