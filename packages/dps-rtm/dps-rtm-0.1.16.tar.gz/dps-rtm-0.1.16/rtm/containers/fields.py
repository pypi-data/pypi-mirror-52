"""This module contains two types of classes: the Fields sequence class, and
the fields it contains. Fields represent the columns (or groups of columns) in
the RTM worksheet."""

# --- Standard Library Imports ------------------------------------------------
import collections
import functools

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import rtm.containers.field as ft
import rtm.main.context_managers as context
import rtm.validate.validation as val
from rtm.main import context_managers as context
from rtm.validate.validator_output import OutputHeader


class Fields(collections.abc.Sequence):

    # --- Collect field classes -----------------------------------------------
    field_classes = []

    @classmethod
    def collect_field(cls):
        """Append a field class to this Fields sequence."""
        def decorator(field_):
            cls.field_classes.append(field_)
            return field_
        return decorator

    # --- Field Object Methods
    def __init__(self):
        """The Fields class is a sequence of fields. First, the field classes
        are collected in the order they're expected to appear in the RTM via
        the `collect_field` decorator. When initialized, all fields in the
        sequence get initialized too."""
        self.height = context.worksheet_columns.get().height  # height is the number of rows of values.
        self._fields = [field_class() for field_class in self.field_classes]

    def get_field_object(self, field_class):
        """Given a field class or name of field class, return the matching
        field object"""
        for _field in self:
            if isinstance(field_class, str):
                if _field.__class__.__name__ == field_class:
                    return _field
            else:
                if isinstance(_field, field_class):
                    return _field
        raise ValueError(f'{field_class} not found in {self.__class__}')

    def validate(self):
        """Validate all field objects in this sequence."""
        for field in self:
            field.validate()

    def print(self):
        """Output validation results to console for field objects in sequence"""
        for field_ in self:
            field_.print()

    # --- Sequence ------------------------------------------------------------
    def __getitem__(self, item):
        return self._fields[item]

    def __len__(self) -> int:
        return len(self._fields)


@Fields.collect_field()
class ID(ft.Field):

    def __init__(self):
        """The ID field uniquely identifies each row (work item) and should
        sort alphabetically in case the excel sheet gets accidentally sorted on
        some other column."""
        super().__init__(name="ID")

    def validate(self):
        """Validate this field"""
        work_items = context.work_items.get()
        self._val_results = [
            OutputHeader(self.name),
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                # No need for explicit "not empty" check b/c this is caught by pxxx
                #   format and val_match_parent_prefix.
                val.val_unique_values(self.values),
                val.val_alphabetical_sort(self.values),
                val.val_root_id_format(self.values, work_items),
                val.val_nonroot_ids_start_w_root_id(),
            ]


@Fields.collect_field()
class CascadeBlock(ft.Field):

    def __init__(self):
        """The CascadeBlock is the most complicated of the RTM fields. it spans
        multiple columns and must help determine the parent for each work item."""
        self.name = 'Cascade Block'
        self._subfields = []
        for subfield_name in self._get_subfield_names():
            subfield = ft.Field(subfield_name)
            if subfield.found:
                self._subfields.append(subfield)
            else:
                self.last_field_not_found = subfield_name
                break

    @staticmethod
    def _get_subfield_names():
        """Return list of column headers. The first several are required. The
        last dozen or so are unlikely to be found on the RTM. This is because
        the user is allowed as many Design Output Solutions as they need."""
        field_names = ["Procedure Step", "Need", "Design Input"]
        for i in range(1, 20):
            field_names.append(f"Solution Level {str(i)}")
        return field_names

    @property
    def found(self):
        """True if at least one RTM column was found matching the headers
        given by self._get_subfield_names"""
        if len(self) > 0:
            return True
        else:
            return False

    @property
    def values(self):
        """Return a list of lists of cell values (for rows 2+)"""
        return [subfield.values for subfield in self]

    @property
    def position_left(self):
        """Return position of the first subfield"""
        if self.found:
            return self[0].position_left
        else:
            return -1

    @property
    def position_right(self):
        """Return position of the last subfield"""
        if self.found:
            return self[-1].position_left
        else:
            return -1

    # @functools.lru_cache()
    # TODO how often does get_row get used? If more than once, add lru cache back in?
    def get_row(self, index) -> list:
        return [col[index] for col in self.values]

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),  # Start with header
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cascade_block_not_empty(),
                val.val_cascade_block_only_one_entry(),
                val.val_cascade_block_x_or_f(),
                val.val_cascade_block_use_all_columns(),
            ]

    # --- Sequence ------------------------------------------------------------
    def __len__(self):
        return len(self._subfields)

    def __getitem__(self, item):
        return self._subfields[item]


@Fields.collect_field()
class CascadeLevel(ft.Field):

    def __init__(self):
        """The Cascade Level field goes hand-in-hand with the Cascade Block. It
        even duplicates some information to a degree. It's important that the
        values in this field agree with those in the Cascade Block."""
        super().__init__(name="Cascade Level")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values),
                val.valid_cascade_levels(self),
                val.val_matching_cascade_levels(),
            ]


@Fields.collect_field()
class ReqStatement(ft.Field):

    def __init__(self):
        """The Requirement Statement field is basically a large text block.
        Besides the req statement itself, it also contains tags, such as for
        marking additional parents and children."""
        super().__init__("Requirement Statement")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
            ]


@Fields.collect_field()
class ReqRationale(ft.Field):

    def __init__(self):
        """This field has very few requirements."""
        super().__init__(name="Requirement Rationale")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values),
            ]


@Fields.collect_field()
class VVStrategy(ft.Field):

    def __init__(self):
        """The V&V Strategy field is subject to few rules."""
        super().__init__(name="Verification or Validation Strategy")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values)
            ]


@Fields.collect_field()
class VVResults(ft.Field):

    def __init__(self):
        """Verification or Validation Results field"""
        super().__init__(name="Verification or Validation Results")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),  # Start with header
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
            ]


@Fields.collect_field()
class Devices(ft.Field):

    def __init__(self):
        """Devices field"""
        super().__init__(name="Devices")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),  # Start with header
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values),
            ]


@Fields.collect_field()
class DOFeatures(ft.Field):

    def __init__(self):
        """"Design Output Features field"""
        super().__init__(name="Design Output Feature (with CTQ ID #)")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),  # Start with header
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values),
            ]


@Fields.collect_field()
class CTQ(ft.Field):

    def __init__(self):
        """CTQ field"""
        super().__init__(name="CTQ? Yes, No, N/A")

    def validate(self):
        """Validate this field"""
        self._val_results = [
            OutputHeader(self.name),  # Start with header
            val.val_column_exist(self.found),
        ]
        if self.found:
            self._val_results += [
                val.val_column_sort(self),
                val.val_cells_not_empty(self.values),
            ]


def get_expected_field_left(field):
    """Return the field object that *should* come before the argument field object."""
    initialized_fields = context.fields.get()
    index_prev_field = None
    for index, field_current in enumerate(initialized_fields):
        if field is field_current:
            index_prev_field = index - 1
            break
    if index_prev_field is None:
        raise ValueError
    elif index_prev_field == -1:
        return None
    else:
        return initialized_fields[index_prev_field]


if __name__ == "__main__":
    pass
