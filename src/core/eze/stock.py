from loguru import logger
from sqlmodel import Session

from constants import c
from core.db import crud, m
from core.gfinance import get_ticker_attributes


def add_new_stock(session: Session, exchange: str, ticker: str) -> m.StockHistory:
    _ticker = f"{exchange}:{ticker}"
    with c.g_worker_pool.acquire_sheet_id() as sheet_id:
        attrs = get_ticker_attributes(
            ticker=_ticker,
            sheet_id=sheet_id,
        )
        new_stock = crud.create_stock(
            session=session,
            ticker=ticker,
            exchange=exchange,
            name=attrs.name,
            currency=attrs.currency,
        )
        history_entry = crud.add_stock_history_entry(
            session=session,
            stock_id=new_stock.id,
            price=attrs.price,
            price_open=attrs.priceopen,
            high=attrs.high,
            low=attrs.low,
            volume=attrs.volume,
            market_cap=attrs.marketcap,
            trade_time=attrs.tradetime,
            data_delay=attrs.datadelay,
            volume_avg=attrs.volumeavg,
            pe=attrs.pe,
            eps=attrs.eps,
            high52=attrs.high52,
            low52=attrs.low52,
            change=attrs.change,
            beta=attrs.beta,
            change_pct=attrs.changepct,
            close_yesterday=attrs.closeyest,
            shares=attrs.shares,
        )
        return history_entry


def get_or_upsert_latest_stock_entry(
    session: Session,
    exchange: str,
    ticker: str,
) -> m.StockHistory:
    existing_stock: m.Stock | None = crud.get_stock(
        session=session,
        ticker=ticker,
        exchange=exchange,
    )
    if not existing_stock:
        logger.info(f"No stock found for {exchange}:{ticker}")
        return add_new_stock(
            session=session,
            ticker=ticker,
            exchange=exchange,
        )

    last_entry: m.StockHistory | None = crud.get_last_history_entry(
        session=session,
        stock_id=existing_stock.id,
    )
    if last_entry is None:
        logger.info(f"No stock found for {exchange}:{ticker}")
        return add_new_stock(
            session=session,
            ticker=ticker,
            exchange=exchange,
        )
    return last_entry


def get_stock_price(
    session: Session,
    exchange: str,
    ticker: str,
) -> float:
    entry: m.StockHistory = get_or_upsert_latest_stock_entry(
        session=session,
        ticker=ticker,
        exchange=exchange,
    )
    return entry.price
