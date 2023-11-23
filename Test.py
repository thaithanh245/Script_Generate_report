from bs4 import BeautifulSoup

data = []

path = "DLT_report0004.html"

found_date_flag = False

with open(path, "r", encoding="utf8") as file:
    test_report = BeautifulSoup(file, "html.parser")

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
        print(execution_date_string)
        break
    result = td_tag.find(text="Test begin: ")
    if result != None:
        found_date_flag = True
        continue