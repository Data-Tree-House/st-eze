from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from pydantic_settings import BaseSettings


class SheetNames(StrEnum):
    ARGS = "args"
    ALL_ATTRIBUTES = "all_attributes"
    ONE_ATTRIBUTE = "one_attribute"
    HISTORIC_RESULT = "historic_attribute"


class GFAttribute(StrEnum):
    price = "price"
    priceopen = "priceopen"
    high = "high"
    low = "low"
    volume = "volume"
    marketcap = "marketcap"
    tradetime = "tradetime"
    datadelay = "datadelay"
    volumeavg = "volumeavg"
    pe = "pe"
    eps = "eps"
    high52 = "high52"
    low52 = "low52"
    change = "change"
    beta = "beta"
    changepct = "changepct"
    closeyest = "closeyest"
    shares = "shares"
    currency = "currency"


class AttributeResult(BaseSettings):
    price: float
    priceopen: float | None
    high: float | None
    low: float | None
    volume: int | None
    marketcap: int | None
    tradetime: datetime | None
    datadelay: int | None
    volumeavg: int | None
    pe: float | None
    eps: float | None
    high52: float | None
    low52: float | None
    change: float | None
    beta: float | None
    changepct: float | None
    closeyest: float | None
    shares: int | None
    currency: str | None


class GFInterval(StrEnum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"


@dataclass
class GFinanceArgs:
    attribute: GFAttribute
    num_days: int
    interval: GFInterval
    ticker: str


class ExtractErrorMsgFunc(Protocol):
    def __call__(self, msg: str) -> str | None: ...
