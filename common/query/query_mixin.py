from __future__ import annotations
from typing import ClassVar
from django.db.models import QuerySet
from .filters import (
    SelectorSearchFilter,
    SelectorOrderingFilter,
    SelectorFilteringBackend
)

class QueryMixin:
    """
    Provides common query behavior for DRF ViewSets.

    Supports:
    - Selector integration
    - Filtering
    - Search
    - Ordering

    Filtering/search/ordering are handled by DRF backends.
    """

    selector: ClassVar = None
    # ---------------------------------------------------------
    # DRF Query Backends
    # ---------------------------------------------------------

    filter_backends: ClassVar = [
        SelectorFilteringBackend,
        SelectorSearchFilter,
        SelectorOrderingFilter,
    ]


    def get_queryset(self) -> QuerySet:
        """
        Returns queryset from selector.

        Selector handles:
        - select_related
        - prefetch_related
        - base filters
        """
        if self.selector is not None:
            return self.selector.get_queryset()

        return super().get_queryset()