from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from loguru import logger
from pydantic import BaseModel
from sqlmodel import Session

from core.eze import get_stock_price
from core.gfinance import GFinanceBadDataError, GFinanceError
from services.api.dependencies import get_session

router: APIRouter = APIRouter(
    prefix="/stock",
    tags=["stock"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    ticker: str
    exchange: str


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
    session: Annotated[Session, Depends(get_session)],
) -> float:
    try:
        return get_stock_price(
            session=session,
            exchange=q.exchange,
            ticker=q.ticker,
        )
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
