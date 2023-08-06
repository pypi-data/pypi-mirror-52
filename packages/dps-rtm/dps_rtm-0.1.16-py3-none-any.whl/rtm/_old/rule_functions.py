# """
#
# This script serves as a library of functions for FDR validator. These functions are derived from the Validator Rules
# outlined in fdr.docs.README. These functions will be called in validate.validation to analyze the content of specific
# cells and entire columns. Rules that relate to cell/column/row relationships are maintained in XXXXXXX.XXXXXXXX.
#
# Each function has 6 comments before it, the first is which field it is intended for (ID, cascade block, requirement
# statement, etc. ) the second states the type of input, the third states the type of output, the fourth is
# the Validator Rule (from README) that it is intended to apply, the fifth is a description of it's functionality,
# the sixth is the status of testing (see unit.test_validate.test_rule_functions).
#
# # Field: ID, Devices, etc.
# # Input: string, list, etc.
# # Output: Boolean, string, list
# # Validator Rule: use similar verbiage as README for traceability
# # Description: describe in english what the function does
# # Test Status: Incomplete, In-progress, complete
# def function()
#     function body goes here...
#
# """
#
#
# # Field: ID
# # Input: String
# # Output: Boolean
# # Validator Rule: recommended ID formatting for procedure steps and procedure based requirements follow a naming
# #   convention. e.g. P010, P020, etc. for procedure steps and P010-020 for procedure based requirements
# # Description: check that input has a capital P as the first character.
# # Test Status: Complete
# def starts_with_p(value):
#     if value.startswith("P"):
#         return True
#     else:
#         return False
#
#
# # Field: ID (procedure steps only)
# # Input: string
# # Output: boolean
# # Validator Rule: recommended ID formatting for procedure steps follow a naming convention.
# # #   e.g. P010, P020, etc. for procedure steps
# # Description: slices string to ignore first character then checks if the remaining characters are integers
# # Test Status: Complete
# def has_only_digits_after_first(value):
#     return value[1:].isdigit()
#
#
# # Field: ID (procedure steps only)
# # Input: string
# # Output: boolean
# # Validator Rule: recommended ID formatting for procedure steps follow a naming convention.
# # #   e.g. P010, P020, etc. for procedure steps
# # Description: check if string has 3 integers following the first character. First character is omitted
# # Test Status: Complete
# def has_only_three_digits(value):
#     value_sliced = value[1:]
#     if (len(value_sliced) == 3) and (value_sliced.isdigit() is True):
#         return True
#     else:
#         return False
#
#
# # Field: ID (non-procedure steps aka need, input, output, etc.)
# # Input: string
# # Output: boolean
# # Validator rule: recommended ID formatting for requirements follow a naming convention.
# #   e.g. P010-020, P010-030, etc.
# # Description: check if value_at_index has 6 integers following the first character. First char is omitted. Assumes
# #   there is a dash and removes it
# # Test Status: Complete
# def has_only_six_digits(value):
#     # slice string. keep all characters after the first. (removes P)
#     value_slice = value[1:]
#     # removes hyphen from string
#     value_slice = value_slice.replace("-", "")
#     if (len(value_slice) == 6) and (value_slice.isdigit() is True):
#         return True
#     else:
#         return False
#
#
# # Field: ID
# # Input: string
# # Output: boolean
# # Validator rule: recommended ID formatting for requirements follow a naming convention.
# # e.g. P010-020, P010-030, etc.
# # Description: check for hyphen within string, location and number of occurrences don't matter
# # Test Status: Complete
# def has_hyphen(value):
#     if value.find("-") != -1:
#         return True
#     else:
#         return False
#
#
# # Field: ID
# # Input: string
# # Output: boolean
# # Validator rule: recommended ID formatting for requirements follow a naming convention.
# # e.g. P010-020, P010-030, etc.
# # Description: check for hyphen in 4th position within string. ex. "P010-010" by looking for lowest and highest index
# # of hyphen using find() and rfind() respectively and comparing them to expected 4th position.
# # Test Status: Complete
# def has_single_hyphen_positioned(value):
#     if (value.find("-") == 4) and (value.rfind("-") == 4):
#         return True
#     else:
#         return False
#
#
# # Field: Cascade block
# # Input: string
# # Output: boolean
# # Validator Rule: only a capital X or capital F are allowed in the cascade visualizer columns. (B-G in its current form)
# # Description: remove spaces and check for capital X. returns false if any other character is present
# # Test Status: Incomplete
# def is_capital_x(value):
#     # remove whitespace for direct string comparison. e.g. ' X ' becomes 'X'
#     value = value.replace(" ", "")
#     if value == "X":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade block
# # Input: string
# # Output: boolean
# # Validator Rule: only a capital X or capital F are allowed in the cascade visualizer columns. (B-G in its current form)
# # Description: remove spaces and check for lower case X. returns false if any other character is present
# # Test Status: Incomplete
# def is_lower_x(value):
#     # remove whitespace for direct string comparison. e.g. ' x ' becomes 'x'
#     value = value.replace(" ", "")
#     if value == "x":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade block
# # Input: string
# # Output: boolean
# # Validator Rule: only a capital X or capital F are allowed in the cascade visualizer columns. (B-G in its current form)
# # Description: remove spaces and check for capital F. returns false if any other character is present
# # Test Status: Incomplete
# def is_capital_f(value):
#     # remove whitespace for direct string comparison. e.g. ' F ' becomes 'F'
#     value = value.replace(" ", "")
#     if value == "F":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade block
# # Input: string
# # Output: boolean
# # Validator Rule: only a capital X or capital F are allowed in the cascade visualizer columns. (B-G in its current form)
# # Description: remove spaces and check for lower case f. returns false if any other character is present
# # Test Status: Incomplete
# def is_lower_f(value):
#     # remove whitespace for direct string comparison. e.g. ' f ' becomes 'f'
#     value = value.replace(" ", "")
#     if value == "f":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'procedure step' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_procedure_step(value):
#     # remove whitespace at the beginning and end of the string and convert to lower case
#     if value.strip().lower() == "procedure step":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'user need' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_user_need(value):
#     # remove whitespace at the beginning and end of the string and test for value_at_index
#     if value.strip().lower() == "user need":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'risk need' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_risk_need(value):
#     # remove whitespace at the beginning and end of the string and test for value_at_index
#     if value.strip().lower() == "risk need":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'business need' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_business_need(value):
#     # remove whitespace at the beginning and end of the string and test for value_at_index
#     if value.strip().lower() == "business need":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'design input' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_design_input(value):
#     # remove whitespace at the beginning and end of the string and test for value_at_index
#     if value.strip().lower() == "design input":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level defines the type of requirement and can only contain one of the following strings:
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is 'design output' by removing white space at the ends and changing all
# # characters to lowercase for direct string comparison
# # Test Status: Incomplete
# def is_design_output(value):
#     # remove whitespace at the beginning and end of the string and test for value_at_index
#     if value.strip().lower() == "design output":
#         return True
#     else:
#         return False
#
#
# # Field: Cascade level
# # Input: string
# # Output: boolean
# # Validator Rule: cascade level may only be one of the 6 defined types.
# # # procedure step, user need, risk need, business need, design input or design output
# # Description: check if cascade level is one of the approved options by running all previously defined functions
# # that look for cascade level. if only 1 is true, the cascade level cell in that row contains one of the approved values
# # Test Status: Incomplete
# def is_cascade_lvl_approved(value):
#     cascade_list = [
#         is_procedure_step(value),
#         is_user_need(value),
#         is_risk_need(value),
#         is_business_need(value),
#         is_design_input(value),
#         is_design_output(value),
#     ]
#     if cascade_list.count(True) == 1:
#         return True
#     else:
#         return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator Rules: hastags are used to identify parent/child relationships,
# # # functional requirements, mating part requirements, user interface requirements and mechanical properties
# # Description: looks for pound/number symbol in string. returns true if present and not followed by numbers (this is to
# # differentiate relationship hashtag from a windchill number)
# # Test Status: Complete
# def has_hashtag(value):
#     pound_indices = []
#     hashtag_list = []
#     if value.find("#") == -1:
#         return False
#     else:
#         for index, char in enumerate(value):
#             if char == "#":
#                 pound_indices.append(index)
#         for test_idx in pound_indices:
#             hashtag_list.append(value[test_idx + 1:test_idx + 4].isalpha())
#         if any(hashtag_list) is True:
#             return True
#         else:
#             return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: integer (occurrences)
# # Validator Rules: hastags are used to identify parent/child relationships,
# # # functional requirements, mating part requirements, user interface requirements and mechanical properties
# # Description: looks for pound/number symbol in string. counts pound symbols that are followed by 3 letters (this is to
# # differentiate relationship hashtag from a windchill number)
# # Test Status: Complete
# def count_hashtags(value):
#     pound_indices = []
#     hashtag_list = []
#     if value.find("#") == -1:
#         return 0
#     else:
#         for index, char in enumerate(value):
#             if char == "#":
#                 pound_indices.append(index)
#         for test_idx in pound_indices:
#             hashtag_list.append(value[test_idx + 1:test_idx + 4].isalpha())
#         return hashtag_list.count(True)
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: The requirement statement can be tagged using #Function to identify a functional requirement
# # Description: checks for #Function in cell by converting to lower case and using direct string comparison.
# # Test Status: Complete
# def has_hashtag_function(value):
#     if value.lower().find("#function") != -1:
#         return True
#     else:
#         return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: The requirement statement can be tagged using #MatingParts to identify a requirement pertaining to
# # proper fitting between components
# # Description: checks for #MatingParts by converting to lower case and using direct string comparison.
# # Test Status: Complete
# def has_hashtag_mating_parts(value):
#     if value.lower().find("#matingparts") != -1:
#         return True
#     else:
#         return False
#
#
# ##TODO Bookmark1 - info below
# """
# BOOKMARK1 - Above this line, all functions have been tested in test_rule_functions and have uniform comments that relate
#             to README. next actions are to continue to revise functions, write uniform comments and resume testing.
# """
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: The requirement statement can be tagged using #MechProperties to identify a requirement that
# #   pertains to the mechanical properties of the implant/instrument
# # Description: checks for #MechProperties by converting to lower case and using direct string comparison. accepts either
# #   #mechproperties or #mechanicalproperties
# # Test Status: Incomplete
# def has_hashtag_mech_properties(value):
#     if value.lower().find("#mechproperties") != -1:
#         return True
#     elif value.lower().find("#mechanicalproperties") != -1:
#         return True
#     else:
#         return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: the requirement statement can be tagged using #UserInterface to identify a requirement that relates
# # to how the user handles the implant/instrument
# # Description: checks for #UserInterface by converting to lower case and using direct string comparison
# # Test Status: Incomplete
# def has_hashtag_user_interface(value):
#     if value.lower().find("#userinterface") != -1:
#         return True
#     else:
#         return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: #Child and #Parent are used to link a Design Input that leads to a Design Output Solution that has
# # been documented earlier in the form. The Design Input is tagged using #Child = P###-### where the ID refers to the
# # Output solution and the Output solution is tagged using #Parent = P###-### where the ID refers to the Design Input
# # Description: checks for #Child returns true if #Child is present by converting to lower case and using direct string
# #   comparison
# # Test Status: Incomplete
# def has_hashtag_child(value):
#     if value.lower().find("#child") != -1:
#         return True
#     else:
#         return False
#
#
# # FDR
# # Field: Requirement Statement
# # Input: string
# # Output: boolean
# # Validator rules: #Child and #Parent are used to link a Design Input that leads to a Design Output Solution that has
# #   been documented earlier in the form. The Design Input is tagged using #Child = P###-### where the ID refers to the
# #   Output solution and the Output solution is tagged using #Parent = P###-### where the ID refers to the Design Input
# # Description: checks for #Parent returns true if #Parent is present by converting to lower case and using direct
# # string comparison
# # Test Status: Incomplete
# def has_hashtag_parent(value):
#     if value.lower().find("#Parent") != -1:
#         return True
#     else:
#         return False
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: list of strings
# # Validator rules: #Child and #Parent are used to link a Design Input that leads to a Design Output Solution that has
# #   been documented earlier in the form. The Design Input is tagged using #Child = P###-### where the ID refers to the
# #   Output solution and the Output solution is tagged using #Parent = P###-### where the ID refers to the Design Input
# # Description: returns IDs (P###-###) that are tagged using #Child as a list. assumes there are #Child present.
# # Test Status: Incomplete
# def retrieve_child_ids(value):
#     # init output list. will append with values later
#     ids_output_list = []
#     # remove spaces for easier evaluation
#     value = value.replace(" ", "")
#     # while there are #child in string. string will be sliced after each ID is retrieved
#     while value.lower().find("#child") != -1:
#         # find the index of the #child hashtag (pound symbol)
#         pound_index = value.lower().find("#child")
#         value = value[pound_index:]
#         # find the beginning of the ID by searching for P
#         id_start_index = value.find("P")
#         # append output list with ID
#         ids_output_list.append(value[id_start_index:id_start_index + 7])
#         value = value[id_start_index:]
#     return ids_output_list
#
#
# # Field: Requirement Statement
# # Input: string
# # Output: list of strings
# # Validator rules: #Child and #Parent are used to link a Design Input that leads to a Design Output Solution that has
# #   been documented earlier in the form. The Design Input is tagged using #Child = P###-### where the ID refers to the
# #   Output solution and the Output solution is tagged using #Parent = P###-### where the ID refers to the Design Input
# # Description: returns IDs (P###-###) that are tagged using #Parent as a list. assumes there are #Parent present.
# # Test Status: Incomplete
# def retrieve_parent_ids(value):
#     # init output list. will append with values later
#     ids_output_list = []
#     # remove spaces for easier evaluation
#     value = value.replace(" ", "")
#     # while there are #child in string. string will be sliced after each ID is retrieved
#     while value.lower().find("#parent") != -1:
#         # find the get_index of the child hashtag
#         hash_index = value.lower().find("#parent")
#         # slice value_at_index from the hash_index + 2 (to account for "P" at the beginning of Parent) to the end
#         value = value[hash_index + 2:]
#         # find the beginning of the ID by searching for P
#         id_start_index = value.find("P")
#         # append output list with ID
#         ids_output_list.append(value[id_start_index:id_start_index + 7])
#         value = value[id_start_index:]
#     return ids_output_list
#
#
# ##TODO Bookmark2 - see info below
# """
# between bookmarks 1 and 2, comments are revised and uniform. once testing is complete, replace bookmark2 with bookmark1.
# """
#
#
# # V&V Results
# # check if W/C,wc or windchill is present. should indicate if windchill number is present
# # FDR rules: Design inputs and outputs may reference a document in windchill for its verification/validation results
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def has_w_slash_c(value):
#     # convert input argument to all lower case for comparison
#     val_lower = value.lower()
#     if val_lower.find("w/c") != -1:
#         return True
#     elif val_lower.find("wc") != -1:
#         return True
#     elif val_lower.find("windchill") != -1:
#         return True
#     else:
#         return False
#
#
# # V&V
# # check if 10 digit windchill number is present. example W/C# 0000006634
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def is_windchill_number_present(value):
#     # remove all spaces
#     value = value.replace(" ", "")
#     # find get_index of 000. windchill numbers have at least three leading zeros.
#     leading_zeros_index = value.find("000")
#     # slice the string starting at that get_index until the end of the string
#     value = value[leading_zeros_index:]
#     # slice string again into two parts. first 10 characters (possible WC number) and remaining characters
#     wc_number = value[:9]
#     remaining_char = value[10:]
#     # test if wc_number is all set_and_get_funcs and remaining is all letters
#     if wc_number.isdigit() and (remaining_char.isalpha() or len(remaining_char) == 0) is True:
#         return True
#     else:
#         return False
#
#
# # Design Output Feature
# # check for CTQ IDs. returns true if "CTQ" is present in the cell
# # FDR rules: CTQ (critical to quality) features should be called out in the Design Output features column.
# # CTQs should be called out using the following format: (CTQ08)
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def has_ctq_id(value):
#     if value.lower().find("ctq") != -1:
#         return True
#     else:
#         return False
#
#
# # Design Output Features
# # check for CTQ number after CTQ tag. returns true if all occurrences of CTQ are followed by two set_and_get_funcs
# # returns false if no CTQs are present OR they are not followed by two set_and_get_funcs. (this should be used in conjunction
# # with the previous function that looks for CTQ in the cell to eliminate possibility of the former case)
# # FDR rules: CTQ (critical to quality) features should be called out in the Design Output features column.
# # CTQs should be called out using the following format: (CTQ08)
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def has_ctq_numbers(value):
#     ctq_count = 0
#     number_count = 0
#     # find get_index of first CTQ ID
#     ctq_index = value.lower().find("ctq")
#     # while loop will keep searching for CTQ IDs until there are none. the string is sliced, checked for set_and_get_funcs,
#     # searched for a new ID, get_index found for new CTQ ID, repeat.
#     while ctq_index != -1:
#         # add 1 to ctq_counter, if there were no CTQs, the while condition would not be met.
#         ctq_count += 1
#         # slice value_at_index from after "ctq"
#         value = value[ctq_index + 3:]
#         # if the next two characters are numbers (they should be if formatted correctly)
#         if value[0:2].isdigit() is True:
#             # add 1 to number counter. this counter will be compared to ctq_count later. they should match
#             number_count += 1
#         # search for next CTQ. if there are not, find() will output a -1 and while loop will end
#         ctq_index = value.lower().find("ctq")
#     # if "ctq" and number count match AND they aren't zero...they are formatted correctly.
#     if (ctq_count == number_count) and ctq_count > 0:
#         return True
#     else:
#         return False
#
#
# # Any
# # check if value_at_index is yes
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def is_yes(value):
#     # remove whitespace for direct string comparison. e.g. 'yes ' becomes 'yes'
#     value = value.replace(" ", "")
#     if value.lower() == "yes":
#         return True
#     else:
#         return False
#
#
# # Any
# # check if value_at_index is no
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def is_no(value):
#     # remove whitespace for direct string comparison. e.g. 'no ' becomes 'no'
#     value = value.replace(" ", "")
#     if value.lower() == "no":
#         return True
#     else:
#         return False
#
#
# # Any
# # check if value_at_index is N/A.
# # FDR rules: type of requirement/other circumstances may/may not allow N/A in certain fs
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def is_notapplic(value):
#     # remove whitespace for direct string comparison. e.g. 'n / a ' becomes 'n/a'
#     value = value.replace(" ", "")
#     # compare lower case version of cell contents to 'n/a'.
#     if value.lower() == "n/a":
#         return True
#     else:
#         return False
#
#
# # Any
# # check if value_at_index is explicitly a hyphen
# # FDR rules: if row is a procedure step, all columns besides ID, cascade visualizer, cascade level and requirement
# #   statement should be a hyphen
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def is_hypen(value):
#     # remove whitespace for direct string comparison. e.g. ' - ' becomes '-'
#     value = value.replace(" ", "")
#     if value == "-":
#         return True
#     else:
#         return False
#
#
# # Any
# # check if value_at_index contains 'not required' in its text
# # FDR rules: some fs are not required. e.g. validation is not required if requirement is a business need
# # Field:
# # Input:
# # Output:
# # Description:
# # Test Status: Incomplete, In-progress, complete
# def has_not_required(value):
#     if value.lower().find("not required") != -1:
#         return True
#     else:
#         return False
#
#
# """
# SANDBOX
# """
# if __name__ == '__main__':
#     # This is your playground
#     # call function
#     # print result
#
#     testval = "blah blah TBD \n anatomy not required (TBD percentile, etc.). \nFunction #Parent = P40-030 #Parent = P40-040"
#     testout = has_not_required(testval)
#     print(testout)
#     pass
#
# """
#
# # init a mock requirement (row on FDR) for testing
# req1 = dict(iD="P20", procedureStep=" ", userNeed="X", cascadeLevel="DESIGN OUTPUT SOLUTION",
#             requirementStatement="Prepare Patient")
# print("\n")
# print(req1)
# print("\n")
#
# """
