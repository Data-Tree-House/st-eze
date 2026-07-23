from pydantic import BaseModel

from .headers import GLOBAL_HEADERS, RATE_LIMIT_HEADERS


class ErrorMessage(BaseModel):
    detail: str


RATE_LIMIT_RESPONSE = {
    "model": ErrorMessage,
    "description": "Rate limit exceeded.",
    "headers": RATE_LIMIT_HEADERS,
    "content": {
        "application/json": {
            "examples": {
                "rate_limit": {
                    "value": {"detail": "Too many requests"},
                },
            }
        }
    },
}


BAD_STOCK_REQUEST_RESPONSE = {
    "model": ErrorMessage,
    "description": "The request was invalid.",
    "headers": GLOBAL_HEADERS,
    "content": {
        "application/json": {
            "examples": {
                "invalid_ticker": {
                    "summary": "Ticker not found",
                    "value": {"detail": "No data returned for symbol 'APL'"},
                },
            }
        }
    },
}

INTERNAL_SERVER_ERROR_RESPONSE = {
    "model": ErrorMessage,
    "headers": GLOBAL_HEADERS,
    "description": "Internal server error.",
}
