"""
Page number pagination implementation.
"""

from __future__ import annotations
from common.constants.query_params import QueryParams

from math import ceil

from django.conf import settings

from rest_framework.pagination import PageNumberPagination

from .base import BasePaginationMixin


class StandardPagination(
    BasePaginationMixin,
    PageNumberPagination,
):
    """
    Default page number pagination.

    Example:

    /users/?page=2&page_size=20

    """

    page_size = getattr(
        settings,
        "DEFAULT_PAGE_SIZE",
        10,
    )

    page_size_query_param = QueryParams.PAGE_SIZE

    max_page_size = QueryParams.MAX_PAGE_SIZE

    page_query_param = QueryParams.PAGE

    def get_pagination_meta(self):

        page_size = self.get_page_size(
            self.request
        )

        return {
            "count": self.page.paginator.count,

            "page": self.page.number,

            "page_size": page_size,

            "total_pages": ceil(
                self.page.paginator.count
                / page_size
            )
            if page_size
            else 0,

            "next": self.get_next_link(),

            "previous": self.get_previous_link(),
        }