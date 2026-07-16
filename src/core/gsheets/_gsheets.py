from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, TypedDict

import pytz  # type: ignore
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ._utils import parse_error
from .gt import (
    AutoRecalc,
    DateTimeRenderOption,
    Dimension,
    GHttpErrorDetails,
    SpreadsheetResource,
    UpdateValuesResponse,
    ValueInputOption,
    ValueRange,
    ValueRenderOption,
)

if TYPE_CHECKING:
    from ._gauth import GAuth


class SheetMainProperties(TypedDict, total=False):
    title: str  # Sheet Name
    locale: str  # en_US
    autoRecalc: str  # ON_CHANGE
    timeZone: str  # Africa/Johannesburg


class SheetProperty(TypedDict, total=False):
    sheetId: int  # The ID of the sheet. Must be non-negative. This field cannot be changed once set.
    title: str  # The index of the sheet within the spreadsheet.
    index: int
    sheetType: str  # : "A String", # The type of sheet. Defaults to GRID. This field cannot be changed once set


class GSheets:
    """Google Sheets API client for reading and writing spreadsheet data.

    This class provides a high-level interface for interacting with Google Sheets,
    including reading values, writing values, and managing sheet metadata.

    Attributes:
        SERVICE_NAME: The Google API service name ("sheets").
        GSHEETS_API_VERSION: The Google Sheets API version to use.
        GSHEETS_NUM_RETRIES: Number of retries for failed API requests.

    GFinanceArgs:
        g_auth: GAuth instance with valid credentials.
        spreadsheet_id: The ID of the Google Spreadsheet to interact with.

    Raises:
        ValueError: If invalid authentication credentials are provided.
        RuntimeError: If the spreadsheet doesn't have auto recalc set to ON_CHANGE.

    Example:
        ```python
        from core.gsheets.gsheets import GAuth, GSheets
        from pathlib import Path

        # Authenticate and create client
        auth = GAuth(credentials_path=Path("service-account.json"))
        sheets = GSheets(auth, spreadsheet_id="your-spreadsheet-id")

        # Read values
        values = sheets.read_values("Sheet1!A1:B10")

        # Write values
        sheets.write_values("Sheet1!A1", [[1, 2], [3, 4]])
        ```
    """

    SERVICE_NAME: str = "sheets"
    GSHEETS_API_VERSION: str = str(os.getenv("GSHEETS_API_VERSION") or "v4")

    # https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.HttpRequest-class.html
    GSHEETS_NUM_RETRIES: int = int(os.getenv("GSHEETS_NUM_RETRIES") or "5")

    def __init__(
        self,
        g_auth: GAuth,
        spreadsheet_id: str,
    ) -> None:
        # How the get and execute works:
        # https://googleapis.github.io/google-api-python-client/docs/start.html#methods-and-requests
        # https://googleapis.github.io/google-api-python-client/docs/start.html#execution-and-response
        self._gauth = g_auth
        self._spreadsheet_id = spreadsheet_id
        self._logger = logging.getLogger("GSheets")

        if not self._gauth.credentials:
            raise ValueError("Invalid Google authentication credentials provided.")

        self._create_service()
        self._describe()

        if self.metadata["properties"]["autoRecalc"] != AutoRecalc.ON_CHANGE:
            raise RuntimeError(
                f"Spreadsheet {self._spreadsheet_id} does not have auto recalc set to ON_CHANGE. "
                "Please update the spreadsheet settings.",
            )

    def _create_service(self) -> None:
        # https://googleapis.github.io/google-api-python-client/docs/start.html#building-and-calling-a-service
        self._service = build(
            # https://googleapis.github.io/google-api-python-client/docs/dyn/
            # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.spreadsheets.html
            serviceName=self.SERVICE_NAME,
            version=self.GSHEETS_API_VERSION,
            credentials=self._gauth.credentials,
            cache_discovery=True,
        )
        # https://developers.google.com/workspace/sheets/api/reference/rest
        self._sheets_client = self._service.spreadsheets()

    def _close_service(self) -> None:
        # https://googleapis.github.io/google-api-python-client/docs/start.html#building-and-calling-a-service
        self._service.close()

    def _describe(self) -> None:
        # If successful, it returns
        # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet
        try:
            # ====> Query
            self.metadata: SpreadsheetResource = self._sheets_client.get(
                spreadsheetId=self._spreadsheet_id,
                includeGridData=False,
                excludeTablesInBandedRanges=True,
            ).execute(
                num_retries=self.GSHEETS_NUM_RETRIES,
            )

            self._logger.info(f"Successfully connected to spreadsheet: {self._spreadsheet_id}")
        except HttpError as e:
            _e: GHttpErrorDetails = parse_error(e)
            self._logger.error(
                f"[{_e['status_code']}] Could not load spreadsheet metadata due to: {_e['reason']}",
                extra=_e,
            )
            raise e

    @property
    def tz(self):
        return pytz.timezone(self.metadata["properties"]["timeZone"])

    def as_datetime(
        self,
        serial_value: float,
    ) -> datetime:
        # expect the date_time_render_option to be in serial mode
        # whole number is the days since December 30th 1899
        # The fractional portion (right of the decimal) counts the time as a fraction of the day
        # We must use self.metadata["timeZone"] (e.g. Africa/Johannesburg) to get it in a nice TZ format
        base_date = datetime(1899, 12, 30, tzinfo=self.tz)
        delta = timedelta(days=serial_value)
        return base_date + delta

    def _create_a1_notation_range(
        self,
        sheet: str,
        cell_range: str | None = None,
    ) -> str:
        # We don't support the 'first visible sheet' functionality
        # For more on the formats:
        # https://developers.google.com/workspace/sheets/api/guides/concepts#cell
        a1_range: str = sheet
        # If no range is specified, we return all the data
        if cell_range is not None:
            a1_range += f"!{cell_range}"
        return a1_range

    def read_cells(
        self,
        sheet: str,
        cell_range: str | None = None,
        major_dimension: Dimension = Dimension.ROWS,
        value_renderer_option: ValueRenderOption = ValueRenderOption.UNFORMATTED_VALUE,
        date_time_render_option: DateTimeRenderOption = DateTimeRenderOption.SERIAL_NUMBER,
        num_retries: int | None = None,
    ) -> ValueRange:
        # https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/get

        a1_range: str = self._create_a1_notation_range(
            sheet=sheet,
            cell_range=cell_range,
        )

        self._logger.debug(
            f"Reading cells from {sheet} with range {cell_range}, major dimension {major_dimension}, "
            f"value renderer option {value_renderer_option}, and date time render option {date_time_render_option}",
        )

        try:
            return (
                self._sheets_client.values()
                .get(
                    spreadsheetId=self._spreadsheet_id,
                    range=a1_range,
                    majorDimension=str(major_dimension),
                    valueRenderOption=str(value_renderer_option),
                    dateTimeRenderOption=str(date_time_render_option),
                )
                .execute(
                    num_retries=num_retries or self.GSHEETS_NUM_RETRIES,
                )
            )
        except HttpError as e:
            _e: GHttpErrorDetails = parse_error(e)
            self._logger.error(
                f"[{_e['status_code']}] Could not read {cell_range=} in {sheet=}: {_e['reason']}",
                extra=_e,
            )
            raise e

    def update_cells(
        self,
        sheet: str,
        body: ValueRange,
        cell_range: str | None = None,
        value_input_option: ValueInputOption = ValueInputOption.USER_ENTERED,
        include_values_in_response: bool = False,
        response_value_render_option: ValueRenderOption = ValueRenderOption.UNFORMATTED_VALUE,
        response_date_time_render_option: DateTimeRenderOption = DateTimeRenderOption.SERIAL_NUMBER,
        num_retries: int | None = None,
    ) -> UpdateValuesResponse:
        # ref: https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/update

        a1_range: str = self._create_a1_notation_range(
            sheet=sheet,
            cell_range=cell_range,
        )

        self._logger.debug(
            f"Updating cells in {sheet} with range {cell_range}",
        )

        try:
            return (
                self._sheets_client.values()
                .update(
                    spreadsheetId=self._spreadsheet_id,
                    range=a1_range,
                    body=body,
                    valueInputOption=str(value_input_option),
                    includeValuesInResponse=include_values_in_response,
                    responseValueRenderOption=str(response_value_render_option),
                    responseDateTimeRenderOption=str(response_date_time_render_option),
                )
                .execute(
                    num_retries=num_retries or self.GSHEETS_NUM_RETRIES,
                )
            )
        except HttpError as e:
            _e: GHttpErrorDetails = parse_error(e)
            self._logger.error(
                f"[{_e['status_code']}] Could not update {cell_range=} in {sheet=}: {_e['reason']}",
                extra=_e,
            )
            raise e
