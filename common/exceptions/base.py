from __future__ import annotations

from typing import Any

from common.constants.error_codes import ErrorCodes
from common.constants.messages import Messages
from rest_framework import status

class BaseApiException(Exception):
    """
    Base exception for all application exceptions.

    These exceptions are framework-agnostic and are translated
    into HTTP responses by the global exception handler.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = Messages.UNEXPECTED_ERROR
    default_error_code: str = ErrorCodes.UNKNOWN_ERROR

    def __init__(
        self,
        *,
        message: str | None = None,
        errors: Any = {},
        meta: Any = {},
        error_code: str | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.errors = errors
        self.meta = meta
        self.error_code = error_code or self.default_error_code

        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the exception into a dictionary.
        """

        payload = {
            "message": self.message,
            "error_code": self.error_code,
        }

        if self.errors is not None:
            payload["errors"] = self.errors

        if self.meta is not None:
            payload["meta"] = self.meta

        return payload