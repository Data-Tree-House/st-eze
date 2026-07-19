from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)
from loguru import logger
from pydantic import BaseModel, Field

from constants import c
from core.gfinance import GFinanceBadDataError, GFinanceError, get_ticker_attributes

router: APIRouter = APIRouter(
    prefix="/stock",
    tags=["stock"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    ticker: str
    exchange: str | None = Field(default=None)


@router.get("/price")
def price(
    q: Annotated[
        FilterParams,
        Query(
            openapi_examples={
                "JSE:SOL": {
                    "summary": "Fetches the price of Sasol from the JSE in ZAC",
                    "description": "When you want an exchange outside the USA, you need to specify the exchange.",
                    "value": {
                        "ticker": "SOL",
                        "exchange": "JSE",
                    },
                }
            }
        ),
    ],
) -> float:
    """Fetches the price of a stock in an exchange. When the exchange is not provided, it will assume it's the USA's
    exchange. Any foreign exchange, like the JSE, will have to be specified."""
    _ticker = q.ticker
    if q.exchange:
        _ticker = f"{q.exchange}:{_ticker}"

    try:
        with c.g_worker_pool.acquire_sheet_id() as sheet_id:
            attrs = get_ticker_attributes(
                ticker=_ticker,
                sheet_id=sheet_id,
            )
            return attrs.price
    except GFinanceBadDataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except GFinanceError as e:
        logger.exception(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Our integration with our stock provider encountered an error. We'll investigate!",
        ) from e
    except Exception as e:
        logger.exception("Encountered an uncaught error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
