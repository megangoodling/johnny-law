import os
import re
import pdf_text_extractor

def remove(string):  # removes double spaces, replaces with single space
    return string.replace("  ", " ")

def get_next_case(my_text):
    # gets filing date A3
    filed_pattern = re.compile(
        r'(Dated:) ([A-Z]\w\w\w\w\w?\w?\w?\w? \d\d?, \d\d\d\d)')
    filed_matches = filed_pattern.finditer(my_text)
    my_filed1 = ""
    for f in filed_matches:
        my_filed1 += str(f.group(2))

    # gets case name B3
    case_name_index = my_text.find("CALIFORNIA")
    # find function must be changed
    case_name_index1 = my_text.find("Defendants.")
    # sometimes there are multiple defendants
    is_division_index = my_text.find("DIVISION")
    my_case_name1 = "".strip()  # removes extra spaces
    if (my_text.find("DIVISION") != -1):  # removes division from name of case
        my_case_name1 = my_text[is_division_index +
                                len("DIVISION"): case_name_index1 + 9].strip()
    else:
        my_case_name1 = my_text[case_name_index +
                                len("CALIFORNIA"): case_name_index1 + 9].strip()

    # gets case number C2
    # case length may vary from case to case
    case_index = my_text.find("Case ")
    my_case_num1 = my_text[case_index + len("Case "): case_index + len("Case ") + 13]

    # gets jurisdiction D2
    # this function will only work for CA
    jurisdiction_index = my_text.find("UNITED STATES")
    jurisdiction_index1 = my_text.find("CALIFORNIA")
    my_jurisdiction1 = remove(my_text[jurisdiction_index:jurisdiction_index1 + 10].strip())

    # gets cause of action E2
    # this will only work for cases that list CAUSE OF ACTION in all caps
    # try to match both CAUSE OF ACTION and Count 1
    action_pattern = re.compile(r'COUNT\s[A-Z][\w|\s|\r.|&|§|,|-]+')
    action_matches = action_pattern.finditer(my_text)
    my_action1 = ""
    for match in action_matches:
        my_action1 += str(match.group(0))

    # gets relief F2
    # this will only work on buxbaum v. zoom
    # use regular expressions to find text
    relief_index = my_text.find("PRAYER FOR RELIEF")
    relief_index1 = my_text.find("Dated: February 27, 2020")
    #my_relief1 = my_text[relief_index + len("relief"): relief_index1]

    next_case_dict = {}
    next_case_dict['my_filed1'] = my_filed1
    next_case_dict['my_case_name1'] = my_case_name1
    next_case_dict['my_case_num1'] = my_case_num1
    next_case_dict['my_jurisdiction1'] = my_jurisdiction1
    next_case_dict['my_action1'] = my_action1
    #next_case_dict['my_relief1'] = my_relief1

    return next_case_dict

