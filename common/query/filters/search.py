from rest_framework.filters import SearchFilter

class SelectorSearchFilter(SearchFilter):

    def get_search_fields(self, view, request):

        selector = getattr(view, "selector", None)

        if selector is None:
            return []

        return selector.searchable_fields