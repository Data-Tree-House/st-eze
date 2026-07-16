from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class SheetNames(StrEnum):
    ARGS = "args"
    RESULT = "result"
    HISTORIC_RESULT = "historic_result"


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
