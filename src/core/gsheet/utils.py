from wolpie import GAuth, GSheets, gt

from .auth import get_client
from .types import Args, GFAttribute, GFInterval, SheetNames


def read_current_args(
    sheet: int = 1,
    g_auth: GAuth | None = None,
):
    g_sheets: GSheets = get_client(sheet=sheet, g_auth=g_auth)

    cell_value: gt.ValueRange = g_sheets.read_cells(
        sheet=SheetNames.ARGS,
    )

    data = dict(cell_value["values"])

    return Args(
        attribute=GFAttribute(data["ATTRIBUTE"]),
        num_days=data["NUM_DAYS"],
        interval=GFInterval(data["INTERVAL"]),
        ticker=data["TICKER"],
    )
