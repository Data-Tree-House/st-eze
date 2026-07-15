# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#    _  m
#  ,`.\/'>
#  (`\<_/`
#    `<<
#
# Author: Johan Hanekom
# Date: February 2026
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

import traceback

from googleapiclient.errors import HttpError

from .gt import GHttpErrorDetails


def parse_error(e: HttpError) -> GHttpErrorDetails:
    return {
        "error_details": e.error_details,
        "reason": e.reason,
        "resp": e.resp,
        "status_code": e.status_code,
        "uri": e.uri,
        "traceback": traceback.format_exc(),
    }  # pyright: ignore[reportReturnType]
