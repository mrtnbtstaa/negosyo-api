from __future__ import annotations

from typing import Any
from rest_framework import status
from rest_framework.response import Response
from ..constants.messages import Messages
from .base import BaseResponse

class OkResponse(Response):
    """
        HTTP 200 Success
    """
    def __init__(
        self,
        data=None,
        message=Messages.OK,
        meta=None,
    ):
        super().__init__(
            data={
                "success": True,
                "message": message,
                "data": data if data is not None else {},
                "meta": meta if meta is not None else {},
            },
            status=status.HTTP_200_OK,
        )


class CreatedResponse(BaseResponse):
    """
    HTTP 201 Created
    """

    def __init__(
        self,
        *,
        data: Any = None,
        message: str = Messages.CREATED,
        meta: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_201_CREATED,
            success=True,
            message=message,
            data=data,
            meta=meta,
        )


class NoContentResponse(Response):
    """
    HTTP 204 No Content

    RFC 9110:
    A 204 response must not include a message body.
    """

    def __init__(self) -> None:
        super().__init__(
            status=status.HTTP_204_NO_CONTENT
        )