"""Test all funcs in rtm.validate.checks"""

import collections
import pytest
import rtm.validate.checks as checks


def test_cell_empty():
    """checks.cell_empty is tested indirectly via test_validation.test_cells_not_empty
    No need to checks it again here.
    """
    pass


# --- Test id_prefix_format ---------------------------------------------------
InputCase = collections.namedtuple('InputCase', 'value expected_result')


@pytest.mark.parametrize('self_id', [
    InputCase('P123-1230', True),
    InputCase('P123', True),
    InputCase(True, False),
    InputCase(False, False),
    InputCase('123', False),
    InputCase(123, False),
    InputCase(None, False),
])
@pytest.mark.parametrize('root_id', [
    InputCase('P123', True),
    InputCase('P1234', False),
    InputCase(True, False),
    InputCase(False, False),
    InputCase('456', False),
    InputCase(456, False),
    InputCase(None, False),
])
def test_id_prefix_format(self_id, root_id):
    expected_result = self_id.expected_result and root_id.expected_result
    assert expected_result == checks.id_prefix_format(self_id.value, root_id.value)
