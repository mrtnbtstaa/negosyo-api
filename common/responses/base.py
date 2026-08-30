from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response


class BaseResponse(Response):
    """
    Base response class for all API responses.

    This class is responsible only for constructing and returning
    a standardized HTTP response.

    Child classes determine the payload structure.
    """

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_200_OK,
        **payload: Any,
    ) -> None:
        super().__init__(
            data=payload,
            status=status_code,
        )