from enum import StrEnum


class HeaderKey(StrEnum):
    process_time = "X-Process-Time"
    last_updated_at = "X-Last-Updated-At"
    retry_after = "Retry-After"

    content_length = "Content-Length"
    content_type = "Content-Type"
    date = "date"
    server = "server"


GLOBAL_HEADERS = {
    HeaderKey.process_time: {"description": "How long it took to process the request", "schema": {"type": "float"}},
    HeaderKey.content_length: {"description": "Length of the response body in bytes", "schema": {"type": "int"}},
    HeaderKey.content_type: {"description": "Response media type", "schema": {"type": "string"}},
    HeaderKey.date: {"description": "Timestamp when the server generated the response", "schema": {"type": "string"}},
    HeaderKey.server: {"description": "Software serving the request"},
}

LAST_UPDATED_AT_HEADER = {
    HeaderKey.last_updated_at: {"description": "ISO formatted last updated at", "schema": {"type": "iso-string"}}
}

RATE_LIMIT_HEADERS = {
    HeaderKey.retry_after: {
        "description": "Seconds until retry.",
        "schema": {"type": "integer"},
    }
} | GLOBAL_HEADERS
