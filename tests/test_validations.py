from typing import Any

import pytest

from core.gfinance.exceptions import GFinanceBadDataError, GFinanceError
from core.gfinance.validations import validate_cell_output, validate_num_columns


@pytest.mark.parametrize(
    ("kwargs", "exception"),
    [
        pytest.param(
            {
                "data": [
                    ["A1", "B1"],
                    ["A1", "B1"],
                ],
                "num_columns": 2,
            },
            None,
            id="2 Columns",
        ),
        pytest.param(
            {
                "data": [
                    ["A1", "B1"],
                    ["A1", "B1", "", "oops"],
                ],
                "num_columns": 2,
            },
            {
                "e": GFinanceError,
                "regex": r"Expected 2 column\(s\), got 4 in row 2",
            },
            id="Expected 2 Columns, got 4",
        ),
        pytest.param(
            {
                "data": [],
                "num_columns": 2,
            },
            {
                "e": GFinanceError,
                "regex": r"Expected 2 column\(s\), got 0",
            },
            id="Expected 2 Columns, got 0",
        ),
    ],
)
def test_validate_num_columns(
    kwargs: dict,
    exception: dict | None,
):
    if exception is not None:
        with pytest.raises(exception["e"], match=exception["regex"]):
            validate_num_columns(**kwargs)
        return
    validate_num_columns(**kwargs)


@pytest.mark.parametrize(
    ("input_value", "exception"),
    [
        pytest.param(
            "#N/A (When evaluating GOOGLEFINANCE, the query for the symbol: 'APL' returned no data.)",
            {
                "e": GFinanceBadDataError,
                "regex": r"No data returned for symbol 'APL'",
            },
            id="No data returned",
        ),
        pytest.param(
            "#N/A (Function GOOGLEFINANCE parameter 2 value is  invalid for the symbol specified.)",
            {
                "e": GFinanceError,
                "regex": r"Function GOOGLEFINANCE parameter 2 value is\s+invalid for the symbol specified\.",
            },
            id="No match found",
        ),
    ],
)
def test_validate_cell_output(
    input_value: Any,
    exception: dict | None,
):
    if exception is not None:
        with pytest.raises(exception["e"], match=exception["regex"]):
            validate_cell_output(input_value)
        return
    validate_cell_output(input_value)
