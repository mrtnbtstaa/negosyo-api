from __future__ import annotations

from rest_framework.response import Response

from common.constants.messages import Messages


class BasePaginationMixin:
    """
    Provides consistent pagination responses.
    """

    def get_paginated_response(
        self,
        data,
    ):
        return Response(
            {
                "success": True,
                "message": Messages.RETRIEVED,
                "data": data,
                "meta": {
                    "pagination": self.get_pagination_meta()
                },
            }
        )


    def get_pagination_meta(self) -> dict:
        """
        Child pagination classes must implement this.
        """

        raise NotImplementedError