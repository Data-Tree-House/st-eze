from pydantic import BaseModel, Field


class PriceFilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    ticker: str = Field(
        description="Stock ticker",
        example="SOL",
    )
    exchange: str = Field(
        description="Exchange the ticker belongs to, e.g. JSE or NASDAQ",
        example="JSE",
    )
