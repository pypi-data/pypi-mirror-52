# """
#
# Tests for functions in rule_functions.
#
# """
#
# from rtm._old.rule_functions import *
#
#
# def test_starts_with_p():
#     pass_list = ['P000', 'PLLL', ]
#     pass_output = []
#     fail_list = ['J000', '0000', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(starts_with_p(i))
#     for j in fail_list:
#         fail_output.append(starts_with_p(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_only_digits_after_first():
#     pass_list = ['P000', 'P999', '9999', ]
#     pass_output = []
#     fail_list = ['JJJJ', 'P0R0', '', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_only_digits_after_first(i))
#     for j in fail_list:
#         fail_output.append(has_only_digits_after_first(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_only_three_digits():
#     pass_list = ['P000', 'P999', 'J999', ]
#     pass_output = []
#     fail_list = ['P1111', 'P0R0', '', 'P55', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_only_three_digits(i))
#     for j in fail_list:
#         fail_output.append(has_only_three_digits(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_only_six_digits():
#     pass_list = ['P000-666', 'P999000', 'P5-55999', ]
#     pass_output = []
#     fail_list = ['P55-555', 'P5-5555', '', 'P555-55', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_only_six_digits(i))
#     for j in fail_list:
#         fail_output.append(has_only_six_digits(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_hyphen():
#     pass_list = ['P000-666', 'P9990-00', 'P5-559-99', ]
#     pass_output = []
#     fail_list = ['P55555', 'P010', '', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_hyphen(i))
#     for j in fail_list:
#         fail_output.append(has_hyphen(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_single_hyphen_positioned():
#     pass_list = ['P000-666', 'jjjj-jjj', ]
#     pass_output = []
#     fail_list = ['P55-555', 'P5-5555', '', 'P555-555-', "P-111-111"]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_single_hyphen_positioned(i))
#     for j in fail_list:
#         fail_output.append(has_single_hyphen_positioned(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_capital_x():
#     pass_list = ['X', 'X ', ' X', ' X ', 'X  ', ]
#     pass_output = []
#     fail_list = ['x', 'f', '-', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_capital_x(i))
#     for j in fail_list:
#         fail_output.append(is_capital_x(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_lower_x():
#     pass_list = ['x', 'x ', ' x', ' x ', 'x  ', ]
#     pass_output = []
#     fail_list = ['X', 'f', '-', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_lower_x(i))
#     for j in fail_list:
#         fail_output.append(is_lower_x(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_capital_f():
#     pass_list = ['F', 'F ', ' F', ' F ', 'F  ', ]
#     pass_output = []
#     fail_list = ['X', 'f', '-', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_capital_f(i))
#     for j in fail_list:
#         fail_output.append(is_capital_f(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_lower_f():
#     pass_list = ['f', 'f ', ' f', ' f ', 'f  ', ]
#     pass_output = []
#     fail_list = ['X', 'F', '-', '', ' ']
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_lower_f(i))
#     for j in fail_list:
#         fail_output.append(is_lower_f(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_procedure_step():
#     pass_list = ['procedure step', 'PROCEDURE STEP', ' procedure step', 'procedure step ', ' procedure step ', ]
#     pass_output = []
#     fail_list = [' ', 'procedurestep', 'procedure_step', 'procedure stel', 'user need', 'surgical step', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_procedure_step(i))
#     for j in fail_list:
#         fail_output.append(is_procedure_step(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_user_need():
#     pass_list = ['user need', 'USER NEED', ' user need', 'user need ', ' user need ', ]
#     pass_output = []
#     fail_list = [' ', 'userneed', 'user_need', 'users need', 'procedure step', 'need', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_user_need(i))
#     for j in fail_list:
#         fail_output.append(is_user_need(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_risk_need():
#     pass_list = ['risk need', 'RISK NEED', ' risk need', 'risk need ', ' risk need ', ]
#     pass_output = []
#     fail_list = [' ', 'riskneed', 'risk_need', 'risk needs', 'procedure step', 'need', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_risk_need(i))
#     for j in fail_list:
#         fail_output.append(is_risk_need(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_business_need():
#     pass_list = ['business need', 'BUSINESS NEED', ' business need', 'business need ', ' business need ', ]
#     pass_output = []
#     fail_list = [' ', 'businessneed', 'business_need', 'business needs', 'procedure step', 'need', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_business_need(i))
#     for j in fail_list:
#         fail_output.append(is_business_need(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_design_input():
#     pass_list = ['design input', 'DESIGN INPUT', ' design input', 'design input ', ' design input ', ]
#     pass_output = []
#     fail_list = [' ', 'designinput', 'design_input', 'design inputs', 'procedure step', 'input', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_design_input(i))
#     for j in fail_list:
#         fail_output.append(is_design_input(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_design_output():
#     pass_list = ['design output', 'DESIGN OUTPUT', ' design output', 'design output ', ' design output ', ]
#     pass_output = []
#     fail_list = [' ', 'designoutput', 'design_output', 'design outputs', 'procedure step', 'output', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_design_output(i))
#     for j in fail_list:
#         fail_output.append(is_design_output(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_is_cascade_lvl_approved():
#     pass_list = [
#         'design output', 'DESIGN INPUT', ' user need', 'design input ', ' procedure step ', ]
#     pass_output = []
#     fail_list = [' ', 'designoutput', 'user_need', 'design inputs', 'need', 'output', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(is_cascade_lvl_approved(i))
#     for j in fail_list:
#         fail_output.append(is_cascade_lvl_approved(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_hashtag():
#     pass_list = ['\n#MatingParts', 'Instrument A needs to thread into Instrument B\n#MatingParts', '#function', ]
#     pass_output = []
#     fail_list = [' ', '#', 'Instrument A has overall length of 15 mm +/- TBD', 'WC #0000567492', '# Function', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_hashtag(i))
#     for j in fail_list:
#         fail_output.append(has_hashtag(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_count_hashtags():
#     pass_list = ['#Function', 'Instrument A ...with Instrument B\n#MatingParts', '#MatingParts\n#Function\n#Parent', ]
#     pass_output = []
#     fail_list = [' ', '#', 'Instrument A has overall length of 15 mm +/- TBD', 'Windchill #0000768572', '# Function']
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(count_hashtags(i))
#     for j in fail_list:
#         fail_output.append(count_hashtags(j))
#     assert pass_output == [1, 1, 3]
#     assert fail_output == [0, 0, 0, 0, 0]
#
#
# def test_has_hashtag_function():
#     pass_list = ['Instrument A shall have overall length within +/- TBD\n#Function', '#function']
#     pass_output = []
#     fail_list = [' ', '--', 'Instrument A has overall length of 15 mm +/- TBD\n#MatingParts', '#matingparts', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_hashtag_function(i))
#     for j in fail_list:
#         fail_output.append(has_hashtag_function(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True
#
#
# def test_has_hashtag_mating_parts():
#     pass_list = ['Instrument A shall have overall length within +/- TBD\n#MatingParts', '#matingparts']
#     pass_output = []
#     fail_list = [' ', '--', 'Instrument A has overall length of 15 mm +/- TBD\n#Function', '#function', ]
#     fail_output = []
#     for i in pass_list:
#         pass_output.append(has_hashtag_mating_parts(i))
#     for j in fail_list:
#         fail_output.append(has_hashtag_mating_parts(j))
#     assert all(pass_output) is True
#     assert not any(fail_output) is True