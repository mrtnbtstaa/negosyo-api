from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend

class SelectorFilteringBackend(DjangoFilterBackend):

    def get_filterset_class(
        self,
        view,
        queryset=None,
    ):
        selector = getattr(
            view,
            "selector",
            None,
        )

        if selector is None:
            return None

        _fields = selector.filterable_fields

        if not _fields:
            return None

        class SelectorFilterSet(FilterSet):

            class Meta:
                model = queryset.model
                fields = _fields

        return SelectorFilterSet