from __future__ import annotations

from ..exceptions.base import BaseApiException
from .base import BaseResponse

class ErrorResponse(BaseResponse):
    """
    Standard API error response.

    Converts a BaseApiException into the standardized
    API response format.
    """
    
    def __init__(
        self,
        exception: BaseApiException,
    ) -> None:

        payload = exception.to_dict()

        super().__init__(
            success=False,
            message=payload["message"],
            errors=payload.get("errors"),
            meta=payload.get("meta"),
            status_code=exception.status_code,
        )

        self.data["error_code"] = payload["error_code"]


