import pytest

from core.gfinance.exceptions import GFinanceError
from core.gfinance.validations import validate_num_columns


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
