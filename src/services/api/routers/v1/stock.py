from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from loguru import logger
from sqlmodel import Session

from core.eze import get_stock
from core.gfinance import GFinanceBadDataError, GFinanceError
from services.api.dependencies import RateLimit, get_session, gsheet_pool
from services.api.models import PriceFilterParams, StockPrice, error_responses, response_headers

router: APIRouter = APIRouter(
    prefix="/stock",
    tags=["stock"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/price",
    dependencies=[Depends(RateLimit(max_requests=30, window=60))],
    response_model=StockPrice,
    responses={
        status.HTTP_400_BAD_REQUEST: error_responses.BAD_STOCK_REQUEST_RESPONSE,
        status.HTTP_429_TOO_MANY_REQUESTS: error_responses.RATE_LIMIT_RESPONSE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: error_responses.INTERNAL_SERVER_ERROR_RESPONSE,
        status.HTTP_200_OK: {"headers": response_headers.GLOBAL_HEADERS | response_headers.LAST_UPDATED_AT_HEADER},
    },
)
def price(
    q: Annotated[PriceFilterParams, Query()],
    sheet_id: Annotated[str, Depends(gsheet_pool)],
    session: Annotated[Session, Depends(get_session)],
    response: Response,
):
    """Will return the current stock's price in the currency of that exchange. For example,
    stocks on the JSE will be returned in ZAC.

    **Note:** stocks that are not on our system will take long to fetch the first round trip. After that,
    the price will be updated in the background every 20 minutes.

    *The prices are not available in real time.*
    """
    try:
        stock = get_stock(
            session=session,
            sheet_id=sheet_id,
            exchange=q.exchange,
            ticker=q.ticker,
        )
        response.headers[response_headers.HeaderKey.last_updated_at] = stock.created_at.isoformat()
        return StockPrice(
            price=stock.price,
            currency=stock.currency,
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
