from bs4 import BeautifulSoup
import os
import re

class HtmlParser:
    def __init__(self, Canoe_test_report_folder):
        self.Canoe_test_report_folder = Canoe_test_report_folder
        self.test_cases_passed = 0
        self.test_cases_failed = 0
        self.test_cases_ID_not_correct_format = 0
        self.test_cases_not_have_ID = 0
        self.html_report_read = 0

    def get_test_result_all_report(self, input_html_file_database:dict, input_test_cases_result_database:dict):
        test_cases_result = input_test_cases_result_database
        html_file_database = input_html_file_database

        list_all_html_report_files = os.listdir(self.Canoe_test_report_folder)
        for html_report in list_all_html_report_files:
            print(f"Reading test report '{html_report}'...")
            if html_report in html_file_database.keys():
                print(f"Report '{html_report}' skipped, already read!")
                continue
            else:
                html_file_database[html_report] = {}
            if "NEST_TEST" in html_report:
                self.html_report_read += 1
                
                with open(f"{self.Canoe_test_report_folder}\{html_report}", "r", encoding="utf8") as html_report_context:
                    test_report = BeautifulSoup(html_report_context, "html.parser")
                result_table = self._get_result_table(test_report=test_report)
                execution_date_string = self._get_execution_date(test_report=test_report)
                self._get_NEST_test_cases_result(result_table=result_table, 
                                                 html_report_name=html_report, 
                                                 test_cases_result=test_cases_result,
                                                 execution_date=execution_date_string)
            elif ".html" in html_report:
                self.html_report_read += 1
                with open(f"{self.Canoe_test_report_folder}\{html_report}", "r", encoding="utf8") as html_report_context:
                    test_report = BeautifulSoup(html_report_context, "html.parser")
                result_table = self._get_result_table(test_report=test_report)
                execution_date_string = self._get_execution_date(test_report=test_report)
                self._get_test_cases_result(result_table=result_table, 
                                            html_report_name=html_report, 
                                            test_cases_result=test_cases_result,
                                            execution_date=execution_date_string)
        print(f"Done read all html report, num of report read: {self.html_report_read}.")
        self._check_result(test_cases_result)

        return html_file_database, test_cases_result

    def _read_test_result_data_from_html(self, html_report_dir:str):    # CANT USE YET
        """
        @Description: TO DO (CANT USE YET)
        @Input: None
        """
        with open(html_report_dir, "r", encoding="utf8") as html_report_context:
            test_report = BeautifulSoup(html_report_context, "html.parser")
            result_table = self._get_result_table(test_report=test_report)
            execution_date_string = self._get_execution_date(test_report=test_report)
            # self._get_NEST_test_cases_result(result_table=result_table, 
            #                                     html_report_name=html_report, 
            #                                     test_cases_result=test_cases_result,
            #                                     execution_date=execution_date_string)

    def _get_result_table(self, test_report):
        found_table_flag = False

        div_tag = test_report.find_all("div")
        for tag in div_tag:
            if found_table_flag == True:
                test_case_result_table = tag
                break
            if tag.string == "Test Case Results":
                found_table_flag = True
                continue
        result_table = test_case_result_table.find_all("tr")
        
        return result_table

    def _get_execution_date(self, test_report):
        found_date_flag = False

        table_tag = test_report.find_all("table")
        for tag in table_tag:
            if found_date_flag == True:
                date_execute = tag
                break
            if "Test Overview" in tag.get_text():
                found_date_flag = True
                continue
        execution_date_table = date_execute.find_all("td")
        found_date_flag = False
        for td_tag in execution_date_table:
            if found_date_flag == True:
                execution_date_string = td_tag.get_text().split(" ")[0]
                execution_date_string = execution_date_string.replace("-", r"/")
                break
            result = td_tag.find(text="Test begin: ")
            if result != None:
                found_date_flag = True
                continue
        
        return execution_date_string

    def _get_test_cases_result(self, result_table, html_report_name:str, test_cases_result:dict, execution_date:str):
        for row in result_table:
            row_data = self._get_row_data_that_have_test_case_result(row=row)
            if row_data != []:  # not read row that dont have test case pass/fail result
                self._check_TC_ID_format_normal_TC(row_data=row_data, html_report_name=html_report_name)
                self._get_TC_result(row_data=row_data, 
                                    TC_type="Normal", 
                                    html_report_name=html_report_name, 
                                    test_cases_result=test_cases_result, 
                                    execution_date=execution_date)          

    def _get_NEST_test_cases_result(self, result_table, html_report_name:str, test_cases_result:dict, execution_date:str):
        for row in result_table:
            row_data = self._get_row_data_that_have_test_case_result(row=row)
            if row_data != []: # not read row that dont have test case pass/fail result
                self._get_TC_result(row_data=row_data, 
                                    TC_type="NEST", 
                                    html_report_name=html_report_name, 
                                    test_cases_result=test_cases_result, 
                                    execution_date=execution_date)

    def _get_row_data_that_have_test_case_result(self, row):
        """
        @return: row_data, format:  row_data[1] = TC_ID, 
                                    row_data[2] = TC_Name, 
                                    row_data[3] = TC_result
        """
        row_data = []
        result_PositiveResultCell = row.find("td", class_="PositiveResultCell") # find in row that have pass cell
        result_NegativeResultCell = row.find("td", class_="NegativeResultCell") # find in row that have fail cell
        if result_PositiveResultCell != None or result_NegativeResultCell != None:  # if row have either pass cell or fail cell then read
            cells = row.find_all("td")
            for cell in cells:
                row_data.append(cell.get_text().replace("\n", ""))
        return row_data
    
    def _check_TC_ID_format_normal_TC(self, row_data:list, html_report_name:str):
        if "" == row_data[1]:
            print(f"TC '{row_data[2]}' in report '{html_report_name}' doesn't have TC ID!")
            row_data[1] = f"unknow_TC_ID_{self.test_cases_not_have_ID}"
            self.test_cases_not_have_ID += 1
        elif "SWTS" not in row_data[1]:
            print(f"TC ID '{row_data[1]}' for TC '{row_data[2]}' in report '{html_report_name}' not in correct format!")
            self.test_cases_ID_not_correct_format += 1

    def _get_TC_result(self, row_data:list, TC_type:str, html_report_name:str, test_cases_result:dict, execution_date:str):
        if row_data[1] not in test_cases_result.keys():
            test_cases_result[row_data[1]] = {}
            test_cases_result[row_data[1]]["TC_result"] = ""
        test_cases_result[row_data[1]]["TC_name"] = row_data[2]
        test_cases_result[row_data[1]]["TC_execution_date"] = execution_date
        test_cases_result[row_data[1]]["TC_type"] = TC_type
        test_cases_result[row_data[1]]["TC_feature"] = re.sub("_report.+", "", html_report_name)    # get feature name from html report file name
        if(test_cases_result[row_data[1]]["TC_result"].lower() != "pass"):  # only update when previous result is not pass
            test_cases_result[row_data[1]]["TC_result"] = row_data[3]

    def _check_result(self, test_cases_result:dict):
        for TC in test_cases_result.keys():
            if test_cases_result[TC]["TC_result"].lower() == "pass":
                self.test_cases_passed += 1
            if test_cases_result[TC]["TC_result"].lower() == "fail":
                self.test_cases_failed += 1