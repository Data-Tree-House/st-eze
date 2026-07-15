from .exceptions import GFinanceError


def validate_num_columns(data: list[list], num_columns: int) -> None:
    if not data:
        raise GFinanceError(f"Expected {num_columns} column(s), got 0")

    for i, row in enumerate(data, start=1):
        if (actual_len := len(row)) != num_columns:
            raise GFinanceError(f"Expected {num_columns} column(s), got {actual_len} in row {i}")
