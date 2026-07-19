import datetime
from typing import Any
from zoneinfo import ZoneInfo

from loguru import logger
from pydantic import ValidationError

from core.gsheets import GAuth, GSheets, gt

from .auth import get_client
from .exceptions import GFinanceBadDataError, GFinanceError
from .types import AttributeResult, GFAttribute, GFinanceArgs, GFInterval, SheetNames
from .validations import extract_error, validate_cell_output, validate_num_columns, validate_rows_and_columns


def extract_tz_info(g_sheet: GSheets) -> ZoneInfo:
    return ZoneInfo(g_sheet.metadata["properties"]["timeZone"])


def serial_to_datetime(serial_num: float, tz_info: ZoneInfo):
    epoch = datetime.datetime(1899, 12, 30, tzinfo=tz_info)
    return epoch + datetime.timedelta(days=serial_num)


def read_current_args(
    sheet_id: str,
    g_auth: GAuth | None = None,
):
    try:
        g_sheets: GSheets = get_client(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

        cell_value: gt.ValueRange = g_sheets.read_cells(
            sheet=SheetNames.ARGS,
        )
        _data = cell_value["values"]
        validate_num_columns(_data, 2)

        data = dict(_data)

        args = GFinanceArgs(
            attribute=GFAttribute(data["ATTRIBUTE"]),
            num_days=data["NUM_DAYS"],
            interval=GFInterval(data["INTERVAL"]),
            ticker=data["TICKER"],
        )
        logger.debug("Args read successfully", extra={"sheet_id": sheet_id, "sheet_args": args})
        return args
    except (KeyError, ValueError) as e:
        raise GFinanceError(
            message=f"Sheet is likely corrupted: {e}",
            sheet_id=sheet_id,
        ) from e
    except (GFinanceError, GFinanceBadDataError) as e:
        raise e
    except Exception as e:
        logger.exception("Could not read current arguments", extra={"sheet_id": sheet_id})
        raise GFinanceError(
            message=f"An unexpected error occurred while trying to read args: {e}",
            sheet_id=sheet_id,
        ) from e


def read_one_attribute(
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> Any:
    try:
        g_sheets: GSheets = get_client(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

        cell_value: gt.ValueRange = g_sheets.read_cells(
            sheet=SheetNames.ONE_ATTRIBUTE,
        )
        _data = cell_value["values"]
        validate_rows_and_columns(_data, 1, 1)

        result = _data[0][0]

        validate_cell_output(result)
        logger.debug(f"Results read from sheet: {result}", extra={"sheet_id": sheet_id, "result_read": result})
        return result
    except (GFinanceError, GFinanceBadDataError) as e:
        raise e
    except Exception as e:
        logger.exception("Could not read result", extra={"sheet_id": sheet_id})
        raise GFinanceError(
            message=f"An unexpected error occurred while trying to update args: {e}",
            sheet_id=sheet_id,
        ) from e


def read_all_attributes(
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> AttributeResult:
    try:
        g_sheets: GSheets = get_client(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

        cell_value: gt.ValueRange = g_sheets.read_cells(
            sheet=SheetNames.ALL_ATTRIBUTES,
        )
        _data = cell_value["values"]
        validate_rows_and_columns(_data, 20, 2)
        data = dict(_data)

        validate_cell_output(data["price"])

        for attribute, value in data.items():
            if error := extract_error(value):
                logger.warning(f"Error in {attribute=}: {error}. Changing to None.")
                data[attribute] = None
            if attribute == "tradetime":
                tz_info = extract_tz_info(g_sheets)
                data[attribute] = serial_to_datetime(value, tz_info)

        all_attributes: AttributeResult = AttributeResult(**data)

        logger.debug(
            f"All Results read from sheet: {all_attributes}",
            extra={"sheet_id": sheet_id, "result_read": all_attributes.model_dump_json()},
        )
        return all_attributes
    except ValidationError as e:
        logger.exception("Pydantic encountered some validation errors", extra={"errors": e.errors()})
        raise GFinanceError(
            message="Could not parse all attributes",
            sheet_id=sheet_id,
        ) from e
    except (GFinanceError, GFinanceBadDataError) as e:
        raise e
    except Exception as e:
        logger.exception("Could not read result", extra={"sheet_id": sheet_id})
        raise GFinanceError(
            message=f"An unexpected error occurred while trying to update args: {e}",
            sheet_id=sheet_id,
        ) from e


def set_args(
    args: GFinanceArgs,
    sheet_id: str,
    g_auth: GAuth | None = None,
):
    try:
        g_sheets: GSheets = get_client(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

        g_sheets.update_cells(
            sheet=SheetNames.ARGS,
            cell_range="A1",  # like placing the cursor there
            body={
                "values": [
                    ["ATTRIBUTE", args.attribute],
                    ["NUM_DAYS", args.num_days],
                    ["INTERVAL", args.interval],
                    ["TICKER", args.ticker],
                ],
                "majorDimension": gt.Dimension.ROWS,
            },
        )
        logger.debug(f"Arguments set: {args}", extra={"sheet_id": sheet_id, "sheet_args": args})
    except (GFinanceError, GFinanceBadDataError) as e:
        raise e
    except Exception as e:
        logger.exception("Could not set arguments", extra={"sheet_id": sheet_id})
        raise GFinanceError(
            message=f"An unexpected error occurred while trying to update args: {e}",
            sheet_id=sheet_id,
        ) from e


def get_ticker_attributes(
    ticker: str,
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> AttributeResult:
    try:
        args = read_current_args(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )
        args.ticker = ticker

        set_args(
            args,
            sheet_id=sheet_id,
            g_auth=g_auth,
        )
        attrs: AttributeResult = read_all_attributes(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )
        logger.debug(
            f"Ticker {ticker} attributes fetched. Price: {attrs.price:,}",
            extra={"sheet_id": sheet_id, "ticker_attributes": attrs.model_dump_json()},
        )
        return attrs
    except (GFinanceError, GFinanceBadDataError) as e:
        raise e
    except Exception as e:
        logger.exception("Could not get ticker price", extra={"sheet_id": sheet_id})
        raise GFinanceError(
            message=f"An unexpected error occurred while trying to update args: {e}",
            sheet_id=sheet_id,
        ) from e
