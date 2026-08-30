from __future__ import annotations

from typing import Any, ClassVar

from django.db.models import Model, QuerySet

from common.exceptions.api import NotFoundException


class BaseSelector:
    """
    Base selector for database read operations.

    Responsible for:
    - Query optimization
    - Default filtering
    - Searching
    - Database retrieval

    Does not handle:
    - HTTP params
    - Pagination
    - Ordering from request
    """

    model: ClassVar[type[Model] | None] = None

    # ---------------------------------------------------------
    # Query configuration
    # ---------------------------------------------------------
    
    base_filters: ClassVar[dict[str, Any]] = {} # If we want to add a base filter (e.g., soft_delete=True)

    searchable_fields: ClassVar[tuple[str, ...]] = () # Searchable fields (e.g., email, first_name, last_name)

    filterable_fields: ClassVar[dict[str, tuple[str, ...]]] = {}

    ordering_fields: ClassVar[tuple[str, ...]] = () # What client allowed to request

    default_ordering: ClassVar[tuple[str, ...]] = () # Default value ordering
    
    # ---------------------------------------------------------
    # Query optimization
    # ---------------------------------------------------------
    select_related: ClassVar[tuple[str, ...]] = ()

    prefetch_related: ClassVar[tuple[str, ...]] = ()


    # ---------------------------------------------------------
    # Base Query
    # ---------------------------------------------------------

    @classmethod
    def get_queryset(cls) -> QuerySet:

        if cls.model is None:
            raise NotImplementedError(
                f"{cls.__name__} must define model."
            )

        queryset = cls.model.objects.all()

        queryset = cls.apply_base_filters(queryset)

        queryset = cls.apply_select_related(queryset)

        queryset = cls.apply_prefetch_related(queryset)

        return queryset


    @classmethod
    def apply_base_filters(
        cls,
        queryset: QuerySet
    ) -> QuerySet:

        if cls.base_filters:
            queryset = queryset.filter(
                **cls.base_filters
            )

        return queryset


    @classmethod
    def apply_select_related(
        cls,
        queryset: QuerySet
    ) -> QuerySet:

        if cls.select_related:
            queryset = queryset.select_related(
                *cls.select_related
            )

        return queryset


    @classmethod
    def apply_prefetch_related(
        cls,
        queryset: QuerySet
    ) -> QuerySet:

        if cls.prefetch_related:
            queryset = queryset.prefetch_related(
                *cls.prefetch_related
            )

        return queryset

    # ---------------------------------------------------------
    # Retrieve
    # ---------------------------------------------------------

    @classmethod
    def get(
        cls,
        **filters: Any
    ) -> Model:

        obj = (
            cls.get_queryset()
            .filter(**filters)
            .first()
        )

        if obj is None:
            raise NotFoundException(
                meta={
                    "model": cls.model.__name__,
                    "filters": filters,
                }
            )

        return obj


    @classmethod
    def get_or_none(
        cls,
        **filters: Any
    ) -> Model | None:

        return (
            cls.get_queryset()
            .filter(**filters)
            .first()
        )


    @classmethod
    def exists(
        cls,
        **filters: Any,
    ) -> bool:
        """
        Determine whether a record exists.
        """

        return (
            cls.get_queryset()
            .filter(**filters)
            .exists()
        )