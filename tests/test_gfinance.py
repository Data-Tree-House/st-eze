from unittest.mock import Mock, patch

import pytest
from dirty_equals import IsAnyStr, IsNumber, IsNumeric

from constants import c
from core.gfinance import read_current_args, read_one_attribute, set_args
from core.gfinance.exceptions import GFinanceBadDataError
from core.gfinance.finance import GFinanceError, get_ticker_attributes, read_all_attributes
from core.gfinance.types import GFAttribute, GFinanceArgs, GFInterval, SheetNames
from core.gsheets import GAuth, gt


def d_test_read_current_args_integration(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        args = read_current_args(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )

    assert args.num_days == IsNumber()
    assert args.ticker == IsAnyStr()


def d_test_set_args_integration(g_auth: GAuth):
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


def d_test_read_result_integration(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        assert (
            read_one_attribute(
                sheet_id=sheet_id,
                g_auth=g_auth,
            )
            == IsNumeric()
        )


def d_test_get_ticker_price_integration(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        assert (
            get_ticker_attributes(
                ticker="JSE:BAT",
                sheet_id=sheet_id,
                g_auth=g_auth,
            ).price
            == IsNumeric()
        )


def d_test_read_all_attributes_integration(g_auth: GAuth):
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        attributes = read_all_attributes(
            sheet_id=sheet_id,
            g_auth=g_auth,
        )


class TestReadArgs:
    def test_read_current_args(self):
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

    def test_unexpected_sheet_format(self):
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

    def test_bad_data_invalid_enum(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {
            "values": [
                ["ATTRIBUTE", "prices"],
                ["NUM_DAYS", 365],
                ["INTERVAL", "DAILY"],
                ["TICKER", "JSE:SOL"],
            ]
        }

        with (
            pytest.raises(GFinanceError, match=r"Sheet is likely corrupted:.*"),
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            read_current_args(
                sheet_id="",
                g_auth=Mock(),
            )

    def test_bad_data_keyerror(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {
            "values": [
                ["ATTRIBUTE", "prices"],
            ]
        }

        with (
            pytest.raises(GFinanceError, match=r"Sheet is likely corrupted:.*"),
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            read_current_args(
                sheet_id="",
                g_auth=Mock(),
            )


class TestSetArgs:
    def test_set_args(self):
        mock_gsheets = Mock()
        mock_gsheets.update_cells = Mock()

        args = GFinanceArgs(
            attribute=GFAttribute.change,
            num_days=365,
            interval=GFInterval.DAILY,
            ticker="JSE:SOL",
        )

        with (
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            set_args(
                args=args,
                sheet_id="",
                g_auth=Mock(),
            )
        mock_gsheets.update_cells.assert_called_once_with(
            sheet=SheetNames.ARGS,
            cell_range="A1",
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


class TestReadOneAttribute:
    def test_read_result(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {"values": [[1230]]}
        mock_g_auth = Mock()
        sheet_id = "123"

        with patch("core.gfinance.finance.get_client", return_value=mock_gsheets) as mock_get_client:
            result = read_one_attribute(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
            mock_get_client.assert_called_once_with(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
        mock_gsheets.read_cells.assert_called_once_with(sheet="one_attribute")

        assert result == 1230

    def test_too_many_rows(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {"values": [[1230], [10]]}
        mock_g_auth = Mock()
        sheet_id = "123"

        with (
            pytest.raises(GFinanceError, match=r"Expected 1 row\(s\), got 2"),
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            read_one_attribute(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )

    def test_too_many_columns(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {"values": [[1230, 10]]}
        mock_g_auth = Mock()
        sheet_id = "123"

        with (
            pytest.raises(GFinanceError, match=r"Expected 1 column\(s\), got 2 in row 1"),
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            read_one_attribute(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )

    def test_no_data_returned(self):
        mock_gsheets = Mock()
        mock_gsheets.read_cells.return_value = {
            "values": [["#N/A (When evaluating GOOGLEFINANCE, the query for the symbol: 'APL' returned no data.)"]]
        }
        mock_g_auth = Mock()
        sheet_id = "123"

        with (
            pytest.raises(GFinanceBadDataError, match=r"No data returned for symbol 'APL'"),
            patch("core.gfinance.finance.get_client", return_value=mock_gsheets),
        ):
            read_one_attribute(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )


class TestGetTickerPrice:
    def test_get_price(self):
        mock_g_auth = Mock()
        sheet_id = "123"

        read_args = GFinanceArgs(
            attribute=GFAttribute.priceopen,
            num_days=365,
            interval=GFInterval.DAILY,
            ticker="JSE:SOL",
        )
        new_args = GFinanceArgs(
            attribute=GFAttribute.priceopen,
            num_days=365,
            interval=GFInterval.DAILY,
            ticker="JSE:BAT",
        )

        mock_attribute_result = Mock()
        mock_attribute_result.price = 12

        with (
            patch("core.gfinance.finance.read_current_args", return_value=read_args) as mock_read_current_args,
            patch("core.gfinance.finance.set_args") as mock_set_args,
            patch("core.gfinance.finance.read_all_attributes", return_value=mock_attribute_result) as mock_read_result,
        ):
            returned_value = get_ticker_attributes(
                ticker="JSE:BAT",
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
            mock_read_current_args.assert_called_once_with(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
            mock_set_args.assert_called_once_with(
                new_args,
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
            mock_read_result.assert_called_once_with(
                sheet_id=sheet_id,
                g_auth=mock_g_auth,
            )
            assert returned_value.price == 12
