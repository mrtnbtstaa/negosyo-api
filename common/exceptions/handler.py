from __future__ import annotations

import logging

from rest_framework.views import exception_handler as drf_exception_handler

from common.exceptions.exception_mapper import ExceptionMapper
from .api import InternalServerErrorException
from common.responses.error import ErrorResponse


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Global exception handler for the application.

    Handle custom application exceptions.
    Handle mapped Django/DRF exceptions.
    DRF handle anything else it knows.
    Return a standardized 500 response for unexpected errors.
    """

    # ------------------------------------------
    # Custom / mapped exceptions
    # ------------------------------------------

    response = ExceptionMapper.map(exc)

    if response is not None:
        return response

    # ------------------------------------------
    # Let DRF try to handle it
    # ------------------------------------------

    response = drf_exception_handler(exc, context)

    if response is not None:
        return response

    # ------------------------------------------
    # Unexpected exception
    # ------------------------------------------

    logger.exception(
        "Unhandled exception occurred.",
        exc_info=exc,
    )

    logger.error(f"Actual Message: {exc}")
    logger.info(f"Actual Message: {exc}")

    return ErrorResponse(InternalServerErrorException())