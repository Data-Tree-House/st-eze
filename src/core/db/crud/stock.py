import hashlib
import json
from datetime import datetime

from sqlmodel import Session, col, select

from core.db import m


def _compute_history_hash(entry: m.StockHistory) -> str:
    payload = entry.model_dump(
        include={
            "price",
            "price_open",
            "high",
            "low",
            "volume",
            "market_cap",
            "trade_time",
            "data_delay",
            "volume_avg",
            "pe",
            "eps",
            "high52",
            "low52",
            "change",
            "beta",
            "change_pct",
            "close_yesterday",
            "shares",
        }
    )
    dumped = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha1(dumped.encode()).hexdigest()


def create_stock(
    session: Session,
    ticker: str,
    exchange: str,
    name: str | None = None,
    currency: str | None = None,
    expiration: float | None = None,
) -> m.Stock:
    new_stock = m.Stock(ticker=ticker.upper().strip(), exchange=exchange.upper().strip())
    if exchange is not None:
        new_stock.exchange = exchange
    if currency is not None:
        new_stock.currency = currency
    if expiration is not None:
        new_stock.expiration = expiration
    if name is not None:
        new_stock.name = name
    session.add(new_stock)
    session.commit()
    session.refresh(new_stock)
    return new_stock


def get_last_history_entry(
    session: Session,
    stock_id: str,
) -> m.StockHistory | None:
    return session.exec(
        select(m.StockHistory)
        .where(m.StockHistory.stock_id == stock_id)
        .order_by(col(m.StockHistory.created_at).desc())
        .limit(1)
    ).one_or_none()


def add_stock_history_entry(
    session: Session,
    stock_id: str,
    price: float,
    price_open: float | None = None,
    high: float | None = None,
    low: float | None = None,
    volume: int | None = None,
    market_cap: int | None = None,
    trade_time: datetime | None = None,
    data_delay: int | None = None,
    volume_avg: int | None = None,
    pe: float | None = None,
    eps: float | None = None,
    high52: float | None = None,
    low52: float | None = None,
    change: float | None = None,
    beta: float | None = None,
    change_pct: float | None = None,
    close_yesterday: float | None = None,
    shares: int | None = None,
) -> m.StockHistory:
    new_entry = m.StockHistory(
        stock_id=stock_id,
        price=price,
        price_open=price_open,
        high=high,
        low=low,
        volume=volume,
        market_cap=market_cap,
        trade_time=trade_time,
        data_delay=data_delay,
        volume_avg=volume_avg,
        pe=pe,
        eps=eps,
        high52=high52,
        low52=low52,
        change=change,
        beta=beta,
        change_pct=change_pct,
        close_yesterday=close_yesterday,
        shares=shares,
    )
    new_entry.history_hash = _compute_history_hash(new_entry)

    last_entry: m.StockHistory | None = get_last_history_entry(
        session=session,
        stock_id=stock_id,
    )

    if last_entry is not None and last_entry.history_hash == new_entry.history_hash:
        return last_entry  # data unchanged since last entry, skip duplicate

    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    return new_entry


def get_stock(
    session: Session,
    ticker: str,
    exchange: str,
) -> m.Stock | None:
    return session.exec(
        select(m.Stock).where(
            m.Stock.ticker == ticker,
            m.Stock.exchange == exchange,
        )
    ).one_or_none()
