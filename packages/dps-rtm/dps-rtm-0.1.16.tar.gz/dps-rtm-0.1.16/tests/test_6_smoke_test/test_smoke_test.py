"""This just runs the entire RTM Validator to make sure that no errors occur."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.main.api as api


def test_smoke_test(fix_path):

    api.main(path=fix_path)
    assert True
