"""
Unit tests for validation.py functions
"""

# --- Standard Library Imports ------------------------------------------------
from collections import namedtuple

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
import rtm.validate.validation as val
import rtm.main.context_managers as context
from rtm.containers.fields import Fields
from rtm.containers.work_items import WorkItems


# --- General Purpose Validation ----------------------------------------------

def test_column_exist(capsys):
    io = [
        (True, f"\tPass\tFIELD EXIST\n"),
        (False, f"\tError\tFIELD EXIST - Field not found. Make sure your headers exactly match the title shown above.\n"),
    ]
    for item in io:
        result = val.val_column_exist(item[0])
        result.print()
        captured = capsys.readouterr()
        assert captured.out == item[1]


@pytest.mark.parametrize("reverse", [False, True])
def test_column_sort(fix_fields, reverse):

    fields = fix_fields("Procedure Based Requirements")
    scores_should = ["Pass"] * len(fields)

    if reverse:
        fields = list(reversed(fields))
        scores_should = ["Pass"] + ["Error"] * (len(fields) - 1)

    with context.fields.set(fields):
        scores_actual = [val.val_column_sort(field).score for field in fields]

    assert len(scores_actual) > 0
    assert scores_actual == scores_should


def test_cells_not_empty():
    passing_values = [True, False, "hello", 42]
    failing_values = [None, ""]
    values = failing_values + passing_values

    failing_indices = list(range(len(failing_values)))
    results = val.val_cells_not_empty(values)
    assert results.indices == failing_indices


# --- ID ----------------------------------------------------------------------

def test_root_id_format():

    SetupRootID = namedtuple('SetupRootID', 'is_root value expected_pass')
    test_set = [
        SetupRootID(True, 'P123', True),
        SetupRootID(True, 'P123-', False),
        SetupRootID(False, 'P123-', True),
        SetupRootID(False, 'P12fd-', True),
        SetupRootID(True, 'P13-', False),
        SetupRootID(True, None, False),
        SetupRootID(True, False, False),
        SetupRootID(True, True, False),
        SetupRootID(True, 123, False),
    ]

    values = [test_item.value for test_item in test_set]
    work_items = test_set  # the function only needs the depth attribute

    expected_error_indices = [
        index
        for index, test_item in enumerate(test_set)
        if not test_item.expected_pass
    ]
    actual_error_indices = val.val_root_id_format(values, work_items).indices

    assert expected_error_indices == actual_error_indices


def test_unique_values():
    values = 'a g b c d a e f g'.split()
    expected_error_indices = [5, 8]
    assert expected_error_indices == val.val_unique_values(values).indices


def test_alphabetical_sort():
    test_sets = [
        (['a', 'b', 'c'], []),
        (['b', 'a', 'c'], [1]),
        (['c', 'b', 'a'], [1, 2]),
    ]

    for test_set in test_sets:
        input_sequence = test_set[0]
        expected_result_indices = test_set[1]
        assert expected_result_indices == val.val_alphabetical_sort(input_sequence).indices


# def test_nonroot_ids_start_w_root_id():




# --- CASCADE BLOCK Setup -----------------------------------------------------

def get_cascade_level_not_empty():
    fields = context.fields.get()
    cascade_field = fields.get_field_object('CascadeLevel')
    results = val.val_cells_not_empty(cascade_field.values)
    return results


def get_valid_cascade_levels():
    fields = context.fields.get()
    cascade_field = fields.get_field_object('CascadeLevel')
    results = val.valid_cascade_levels(cascade_field)
    return results


CascadeValidation = namedtuple("CascadeValidation", "func header")
cascade_validations = [
    CascadeValidation(func=val.val_cascade_block_not_empty, header="not_empty"),
    CascadeValidation(func=val.val_cascade_block_only_one_entry, header="one_entry"),
    CascadeValidation(func=val.val_cascade_block_x_or_f, header="x_or_f"),
    CascadeValidation(func=get_cascade_level_not_empty, header='cascade_level_not_empty'),
    CascadeValidation(func=get_valid_cascade_levels, header='cascade_level_valid_input'),
    CascadeValidation(func=val.val_matching_cascade_levels, header='cascade_level_matching'),
    CascadeValidation(func=val.val_nonroot_ids_start_w_root_id, header='non_root_ids_start_w_root_id'),
]


# --- CASCADE BLOCK -----------------------------------------------------------

@pytest.mark.parametrize("cascade_validation", cascade_validations)
def test_rtm_xlsx_cascade(fix_worksheet_columns, cascade_validation: CascadeValidation):

    # Setup
    ws_cols = fix_worksheet_columns("cascade")
    with context.worksheet_columns.set(ws_cols):
        fields = Fields()
    with context.fields.set(fields):
        work_items = WorkItems()

    # Expected result
    col_with_expected_results = cascade_validation.header
    indices_expected_to_fail = [
        index
        for index, value in enumerate(ws_cols.get_first(col_with_expected_results).values)
        if not value
    ]

    # Compare
    val_func = cascade_validation.func
    with context.fields.set(fields), context.work_items.set(work_items):
        indices_that_actually_fail = list(val_func().indices)
    assert indices_that_actually_fail == indices_expected_to_fail


def test_val_cascade_block_use_all_levels(fix_worksheet_columns):

    # Setup
    ws_cols = fix_worksheet_columns("cascade")
    with context.worksheet_columns.set(ws_cols):
        fields = Fields()
    with context.fields.set(fields):
        work_items = WorkItems()

    with context.fields.set(fields), context.work_items.set(work_items):
        assert val.val_cascade_block_use_all_columns().score == "Warning"


def test_val_matching_cascade_levels():
    pass


if __name__ == "__main__":
    pass
