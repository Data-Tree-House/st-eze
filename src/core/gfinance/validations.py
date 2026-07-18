import re
from typing import Any

from .exceptions import GFinanceBadDataError, GFinanceError
from .types import ExtractErrorMsgFunc

CELL_ERROR_PATTERN = re.compile(r"^#N\/A\s*\((?P<error_message>.*)\)\s*$", re.IGNORECASE)
NO_DATA_PATTERN = re.compile(r"the\s*symbol:\s*['\"`](?P<symbol>.*)['\"`]\s*returned\s*no\s*data", re.IGNORECASE)


def extract_error(value: Any) -> str | None:
    if match := CELL_ERROR_PATTERN.match(str(value)):
        return match.group("error_message")
    return None


def extract_no_data_error(msg: str) -> str | None:
    if match := NO_DATA_PATTERN.search(msg):
        symbol = match.group("symbol")
        return f"No data returned for symbol {symbol!r}"
    return None


def validate_num_columns(data: list[list], num_columns: int) -> None:
    if not data:
        raise GFinanceError(f"Expected {num_columns} column(s), got 0")

    for i, row in enumerate(data, start=1):
        if (actual_len := len(row)) != num_columns:
            raise GFinanceError(f"Expected {num_columns} column(s), got {actual_len} in row {i}")


def validate_num_rows(data: list[list], num_rows: int) -> None:
    if not data:
        raise GFinanceError(f"Expected {num_rows} row(s), got 0")
    actual_len = len(data)
    if actual_len != num_rows:
        raise GFinanceError(f"Expected {num_rows} row(s), got {actual_len}")


def validate_rows_and_columns(data: list[list], num_rows: int, num_columns: int) -> None:
    validate_num_rows(data, num_rows)
    validate_num_columns(data, num_columns)


def validate_cell_output(value: Any) -> None:
    if not (error_message := extract_error(value)):
        return

    bad_data_checks: list[ExtractErrorMsgFunc] = [extract_no_data_error]

    for error_check in bad_data_checks:
        if matched_error_str := error_check(error_message):
            raise GFinanceBadDataError(message=matched_error_str)

    raise GFinanceError(message=error_message)
