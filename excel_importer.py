"""excel_importer.py"""
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side, Color
import pdf_text_extractor
import next_case

mylines = [] 
my_string = "" 

original_pdf_name = 'buxbaum v zoom.pdf'
my_string = pdf_text_extractor.convert_pdf_to_text(original_pdf_name)
# with open(curFile, 'rt') as myfile:
#     for myline in myfile:
#         mylines.append(myline.rstrip('\n'))
#     for myline1 in myfile:
#         if (myline1 != ""): 
#             mylines.append(myline1)
#     for element in mylines:
#         my_string += str(element) + " "  # turns list into string
    
def remove(string):  # removes double spaces, replaces with single space
    return string.replace("  ", " ")

# gets filing date A2
import re
filed_pattern = re.compile(
    r'(Dated:) ([A-Z]\w\w\w\w\w?\w?\w?\w? \d\d?, \d\d\d\d)')
filed_matches = filed_pattern.finditer(my_string)
my_filed = ""
for f in filed_matches:
    my_filed += str(f.group(2))

# gets case name B2
# this will only work in California # maybe this could be pulled from file name?
case_name_index = my_string.find("CALIFORNIA")
case_name_index1 = my_string.find("Defendant.")
is_division_index = my_string.find("DIVISION")
my_case_name = "".strip()  # removes extra spaces
if (my_string.find("DIVISION") != -1):  # removes division from name of case
    my_case_name = my_string[is_division_index +
                             len("DIVISION"): case_name_index1 + 9].strip()
else:
    my_case_name = my_string[case_name_index +
                             len("CALIFORNIA"): case_name_index1 + 9].strip()

# gets case number C2
# case length may vary from case to case
case_index = my_string.find("Case ")
my_case_num = my_string[case_index +
                        len("Case "): case_index + len("Case ") + 13]

# gets jurisdiction D2
# this function will only work for CA
jurisdiction_index = my_string.find("UNITED STATES")
jurisdiction_index1 = my_string.find("CALIFORNIA")
my_jurisdiction = remove(
    my_string[jurisdiction_index:jurisdiction_index1 + 10].strip())

# gets cause of action E2
# this will only work for cases that list CAUSE OF ACTION in all caps
pattern = re.compile(
    r'.?.?.?.?.?.?. CAUSE OF ACTION\s[A-Z][\w|\s|\r.|&|§|,|-]+')
matches = pattern.finditer(my_string)
my_action1 = ""
for match in matches:
    my_action1 += str(match.group(0))
my_action = remove(my_action1)

# gets relief F2
# this will only work on buxbaum v. zoom
# use regular expressions to find text
relief_index = my_string.find("relief:")
relief_index1 = my_string.find("Dated: April 29, 2020")
my_relief = my_string[relief_index + len("relief"): relief_index1]
# print(my_relief)

workbook = Workbook()
sheet = workbook.active

bold_font = Font(bold=True)
wrap_text = Alignment(wrap_text=True)

sheet["A1"] = "Date of Filing"  # names excel header
sheet["A1"].font = bold_font
sheet["B1"] = "Case Name"
sheet["B1"].font = bold_font
sheet["C1"] = "Case Number"
sheet["C1"].font = bold_font
sheet["D1"] = "Jurisdiction"
sheet["D1"].font = bold_font
sheet["E1"] = "Causes of Action"
sheet["E1"].font = bold_font
sheet["F1"] = "Relief Sought"
sheet["F1"].font = bold_font
sheet["G1"] = "Other/Misc"
sheet["G1"].font = bold_font
# sheet["H1"] = "Other/Misc"  # maybe include a function that asks if the law
# contains a certain value? i.e. notice to cure? returns true/false
# from next_case import my_filed1, my_case_name1, my_case_num1, my_jurisdiction1, my_action1, my_relief1


next_case_dict = next_case.get_next_case(my_string)

sheet["A2"] = next_case_dict['my_filed1']  # inputs value from filed into cell
sheet["B2"] = next_case_dict['my_case_name1']
sheet["C2"] = next_case_dict['my_case_num1']
sheet["D2"] = next_case_dict['my_jurisdiction1']
sheet["E2"] = next_case_dict['my_action1']
#sheet["F2"] = next_case_dict['my_relief1']

# sheet["A3"] = my_filed1
# sheet["B3"] = my_case_name1
# sheet["C3"] = my_case_num1
# sheet["D3"] = my_jurisdiction1
# sheet["E3"] = my_action1
# sheet["F3"] = my_relief1
# sheet["G2"] = my_other1
# create function to append information from the next text
# file into the next excel cells. A4 for next case and
# so on.

# workbook.save(filename="litigation_tracker.xlsx")
