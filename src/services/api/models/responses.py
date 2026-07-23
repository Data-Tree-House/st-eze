from pydantic import BaseModel, Field


class StockPrice(BaseModel):
    price: float = Field(
        description="Current stock price in the exchange's native currency.",
        examples=[512.34],
    )
    currency: str | None = Field(
        description="Currency in which the stock is reported in",
        examples=["ZAC"],
    )
