from __future__ import annotations

from django.conf import settings

from rest_framework.pagination import CursorPagination

from .base import BasePaginationMixin


class CursorPagination(
    BasePaginationMixin,
    CursorPagination,
):
    """
    Cursor based pagination.

    Recommended for:
    - feeds
    - logs
    - large datasets
    """

    page_size = getattr(
        settings,
        "DEFAULT_PAGE_SIZE",
        10,
    )

    page_size_query_param = "page_size"

    max_page_size = 100


    ordering = "-created_at"


    def get_pagination_meta(self):

        return {
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }