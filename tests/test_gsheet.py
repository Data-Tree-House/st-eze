# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#    _  m
#  ,`.\/'>
#  (`\<_/`
#    `<<
#
# Author: Johan Hanekom
# Date: February 2026
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


import logging
import re
from typing import Any

import pytest
import pytz  # type: ignore
from googleapiclient.errors import HttpError

from constants import c
from core.gsheets import GAuth, GSheets, gt

from .utils import get_test_name


def test_init(
    g_auth: GAuth,
):
    g_sheets = GSheets(
        g_auth=g_auth,
        spreadsheet_id=c.g_integration_test_sheet_id,
    )

    # =============== // MAIN PROPERTIES // ===============

    assert g_sheets.metadata["properties"]["title"] == "integration_tests"
    assert g_sheets.metadata["properties"]["locale"] == "en_US"
    assert g_sheets.metadata["properties"]["autoRecalc"] == gt.AutoRecalc.ON_CHANGE
    assert g_sheets.metadata["properties"]["timeZone"] == "Africa/Johannesburg"

    # =============== // SHEETS // ===============

    assert len(g_sheets.metadata["sheets"]) > 0
    assert any(sheet["properties"]["title"] == "test_read_cell" for sheet in g_sheets.metadata["sheets"])


def test_init_error_handling(
    g_auth: GAuth,
    caplog: pytest.LogCaptureFixture,
):
    # ====> SETUP THE LOGGER
    caplog.set_level(logging.ERROR)

    # ====> CHECK THAT AN ERROR IS RAISED
    with pytest.raises(HttpError) as exc_info:
        GSheets(
            g_auth=g_auth,
            spreadsheet_id="iDoNoyExist",
        )

    # ====> CORRECT ERROR RAISED
    assert exc_info.value.status_code == 404

    # ====> CHECK LOGS
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "ERROR"
    assert re.match(r".*404.*Could not load spreadsheet metadata due to", record.message)


@pytest.mark.parametrize(
    ("cell_range", "kwargs", "expected_value"),
    [
        pytest.param(
            "A1",
            {},
            "hello_world",
            id="String",
        ),
        pytest.param(
            "A2",
            {},
            10,
            id="Int",
        ),
        pytest.param(
            "A3",
            {},
            0.3,
            id="Percent",
        ),
        pytest.param(
            "A3",
            {
                "value_renderer_option": gt.ValueRenderOption.FORMATTED_VALUE,
            },
            "30.0%",
            id="Percent (Formatted)",
        ),
        pytest.param(
            "A4",
            {},
            46082.370027372686,
            id="DateTime",
        ),
    ],
)
def test_read_cell(
    cell_range: str | None,
    kwargs: dict,
    expected_value: Any,
    g_auth: GAuth,
    request: pytest.FixtureRequest,
):
    sheet_name: str = get_test_name(request.node.name)

    g_sheets = GSheets(
        g_auth=g_auth,
        spreadsheet_id=c.g_integration_test_sheet_id,
    )

    cell_value: gt.ValueRange = g_sheets.read_cells(
        sheet=sheet_name,
        cell_range=cell_range,
        **kwargs,
    )

    assert cell_value["values"][0][0] == expected_value


def test_read_datetime_cell(
    g_auth: GAuth,
    request: pytest.FixtureRequest,
):
    sheet_name: str = get_test_name(request.node.name)

    g_sheets = GSheets(
        g_auth=g_auth,
        spreadsheet_id=c.g_integration_test_sheet_id,
    )

    cell_value: gt.ValueRange = g_sheets.read_cells(
        sheet=sheet_name,
        cell_range="A1",
    )

    dt = g_sheets.as_datetime(cell_value["values"][0][0])

    # check if it is 1 March 2026 8:52 am and TZ Africa/Johannesburg
    assert dt.year == 2026
    assert dt.month == 3
    assert dt.day == 1
    assert dt.hour == 8
    assert dt.minute == 52
    assert dt.tzinfo == pytz.timezone("Africa/Johannesburg")


def test_read_multiple_cells(
    g_auth: GAuth,
    request: pytest.FixtureRequest,
):
    sheet_name: str = get_test_name(request.node.name)

    g_sheets = GSheets(
        g_auth=g_auth,
        spreadsheet_id=c.g_integration_test_sheet_id,
    )

    cell_value: gt.ValueRange = g_sheets.read_cells(
        sheet=sheet_name,
    )

    header = cell_value["values"].pop(0)
    data = cell_value["values"]

    assert header == ["Name", "Value"]
    assert len(data) == 1020


def test_update_cell(
    g_auth: GAuth,
    request: pytest.FixtureRequest,
):
    sheet_name: str = get_test_name(request.node.name)

    g_sheets = GSheets(
        g_auth=g_auth,
        spreadsheet_id=c.g_integration_test_sheet_id,
    )

    g_sheets.update_cells(
        sheet=sheet_name,
        cell_range="A1",
        body={
            "values": [["updated_value"]],
            "majorDimension": gt.Dimension.ROWS,
        },
    )
