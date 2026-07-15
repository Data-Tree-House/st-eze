from core.gsheets import GAuth, GSheets, gt

from .auth import get_client
from .exceptions import GFinanceError
from .types import Args, GFAttribute, GFInterval, SheetNames
from .validations import validate_num_columns


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

        return Args(
            attribute=GFAttribute(data["ATTRIBUTE"]),
            num_days=data["NUM_DAYS"],
            interval=GFInterval(data["INTERVAL"]),
            ticker=data["TICKER"],
        )
    except ValueError as e:
        raise GFinanceError(
            message=f"A ValueError occurred: {e}",
            sheet_id=sheet_id,
        ) from e


def read_result(
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> int:
    g_sheets: GSheets = get_client(
        sheet_id=sheet_id,
        g_auth=g_auth,
    )

    cell_value: gt.ValueRange = g_sheets.read_cells(
        sheet=SheetNames.RESULT,
    )
    return cell_value["values"][0][0]


def set_args(
    args: Args,
    sheet_id: str,
    g_auth: GAuth | None = None,
):
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


def get_ticker_price(
    ticker: str,
    sheet_id: str,
    g_auth: GAuth | None = None,
) -> int:
    args = read_current_args(
        sheet_id=sheet_id,
        g_auth=g_auth,
    )
    args.attribute = GFAttribute.price
    args.ticker = ticker

    set_args(
        args,
        sheet_id=sheet_id,
        g_auth=g_auth,
    )
    return read_result(
        sheet_id=sheet_id,
        g_auth=g_auth,
    )
