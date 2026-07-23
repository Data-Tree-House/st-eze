GLOBAL_HEADERS = {
    "X-Process-Time": {"description": "How long it took to process the request", "schema": {"type": "float"}}
}

RATE_LIMIT_HEADERS = {
    "Retry-After": {
        "description": "Seconds until retry.",
        "schema": {"type": "integer"},
    }
} | GLOBAL_HEADERS
