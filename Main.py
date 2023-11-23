import sys
import traceback
from config_handler import ConfigHandler
from excel_handler import ExcelHandler
from database_handler import DatabaseHandler

try:
    print("Reading config file ...")
    config_handler = ConfigHandler()
    config_handler.load_config()
    config_handler.clean_up_and_reset_output()
    SWTS_DOORS_info = config_handler.get_excel_SWTS_DOORS()
    TRS_DOORS_info = config_handler.get_excel_TRS_DOORS()
    excel_template_test_report_info = config_handler.get_excel_template_test_report()
    database_folder = config_handler.get_database_folder()
    output_dir = config_handler.get_output_folder()
    print("DONE!")

    #logging_handler = LoggingHandler()
    database_handler = DatabaseHandler(database_dir=database_folder)

    print("Reading SWTS DOORS excel ...")
    excel_handler = ExcelHandler(excel_dir=SWTS_DOORS_info["excel_dir"])
    SWTS_DOORS_dict = excel_handler.get_SWTS_DOORS(SWTS_DOORS_info, "TRS_")
    database_handler.save_SWTS_DOORS_database(database=SWTS_DOORS_dict)
    print("DONE!")

    print("Reading TRS DOORS excel ...")
    excel_handler = ExcelHandler(excel_dir=TRS_DOORS_info["excel_dir"])
    TRS_DOORS_dict = excel_handler.get_TRS_DOORS(TRS_DOORS_info)
    database_handler.save_TRS_DOORS_database(database=TRS_DOORS_dict)
    print("DONE!")

    print("Reading requirement coverage from template report excel ...")
    excel_handler = ExcelHandler(excel_dir=excel_template_test_report_info["excel_dir"])
    TRS_DOORS_dict = excel_handler.read_req_coverage_template_report(excel_template_test_report_info)
    database_handler.save_TRS_DOORS_database(database=TRS_DOORS_dict)
    print("DONE!")

    print("Filling TC to test report and save to output ...")
    excel_handler = ExcelHandler(excel_dir=excel_template_test_report_info["excel_dir"])
    excel_handler.fill_test_report_save_to_output(excel_template_test_report_info, database_handler, output_dir)
    print("DONE!")

    print("Test Report have been generated, please find the reports in the output folder.")

    input("Press Enter to continue ......")
except Exception as error:
    traceback.print_exc()
    input("Press Enter to continue ......")
    sys.exit(error)
    