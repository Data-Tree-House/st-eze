from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsAnyStr, IsNumber, IsNumeric

from constants import c
from core.gfinance import read_current_args, read_result, set_args
from core.gfinance.finance import GFinanceError, get_ticker_price
from core.gsheets import GAuth


def test_read_current_args_integration(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        args = read_current_args(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

    assert args.num_days == IsNumber()
    assert args.ticker == IsAnyStr()


def test_read_current_args():
    mock_gsheets = Mock()
    mock_gsheets.read_cells.return_value = {
        "values": [
            ["ATTRIBUTE", "price"],
            ["NUM_DAYS", 365],
            ["INTERVAL", "DAILY"],
            ["TICKER", "JSE:SOL"],
        ]
    }
    mock_g_auth = Mock()
    sheet_id = "123"

    with patch("core.gfinance.finance.get_client", return_value=mock_gsheets) as mock_get_client:
        args = read_current_args(
            sheet_id=sheet_id,
            g_auth=mock_g_auth,
        )
        mock_get_client.assert_called_once_with(
            sheet_id=sheet_id,
            g_auth=mock_g_auth,
        )
    mock_gsheets.read_cells.assert_called_once_with(sheet="args")

    assert args.num_days == IsNumber()
    assert args.ticker == IsAnyStr()


def test_read_current_args_unexpected_sheet_format():
    mock_gsheets = Mock()
    mock_gsheets.read_cells.return_value = {
        "values": [
            ["ATTRIBUTE", "price"],
            ["NUM_DAYS", 365],
            ["INTERVAL", "DAILY", "", "", "not-valid"],
            ["TICKER", "JSE:SOL"],
        ]
    }

    with (
        pytest.raises(GFinanceError, match=r"Expected 2 column\(s\), got 5 in row 3"),
        patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
    ):
        read_current_args(
            sheet_id="",
            g_auth=Mock(),
        )


def test_set_args(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        args = read_current_args(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )
        args.ticker = "JSE:SOL"

        set_args(
            args,
            sheet_id=sheet_id,
            g_auth=g_auth,
        )


def test_read_result(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        assert (
            read_result(
                sheet_id=sheet_id,
                g_auth=g_auth,
            )
            == IsNumeric()
        )


def test_get_ticker_price(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        assert (
            get_ticker_price(
                ticker="JSE:BAT",
                sheet_id=sheet_id,
                g_auth=g_auth,
            )
            == IsNumeric()
        )
