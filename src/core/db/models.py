import uuid
from datetime import UTC, datetime

from sqlalchemy import Engine
from sqlmodel import Field, Relationship, SQLModel


def generate_id(table_name: str) -> str:
    return f"{table_name}_{uuid.uuid7()}"


def utc_now() -> datetime:
    return datetime.now(UTC)


class TableBase(SQLModel):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={
            "onupdate": utc_now,
        },
    )


class Stock(TableBase, table=True):
    __tablename__ = "stock"
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        default_factory=lambda: generate_id(Stock.__tablename__),
        primary_key=True,
        index=True,
        nullable=False,
    )
    ticker: str
    exchange: str
    name: str | None = Field(default=None)
    currency: str | None = Field(default=None)
    expiration: float = Field(default=20 * 60)  # sec

    stock_history: list["StockHistory"] = Relationship(back_populates="stock")  # noqa: UP037


class StockHistory(TableBase, table=True):
    __tablename__ = "stock_history"
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        default_factory=lambda: generate_id(StockHistory.__tablename__),
        primary_key=True,
        index=True,
        nullable=False,
    )
    stock_id: str | None = Field(default=None, foreign_key="stock.id")
    history_hash: str = Field(index=True, default="")

    price: float
    price_open: float | None
    high: float | None
    low: float | None
    volume: int | None
    market_cap: int | None
    trade_time: datetime | None
    data_delay: int | None
    volume_avg: int | None
    pe: float | None
    eps: float | None
    high52: float | None
    low52: float | None
    change: float | None
    beta: float | None
    change_pct: float | None
    close_yesterday: float | None
    shares: int | None
    currency: str | None

    stock: Stock | None = Relationship(back_populates="stock_history")


def create_all_tables(engine: Engine):
    SQLModel.metadata.create_all(
        engine,
        checkfirst=True,
    )
